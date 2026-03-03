"""
需求提取模块
"""
from typing import Optional, Dict, Any, Tuple
import json
from openai import OpenAI
from models.requirement import Requirement
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME, MAX_TOKENS, TEMPERATURE
from utils.logger import log_info, log_error, log_warning


class RequirementExtractor:
    """需求提取器，用于从自然语言中提取租房需求"""
    
    def __init__(self):
        """初始化需求提取器"""
        self.client = None
        if OPENAI_API_KEY:
            self.client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL if OPENAI_BASE_URL else None
            )
        self.conversation_history = []
    
    def extract_requirement(self, user_input: str, current_requirement: Optional[Requirement] = None) -> Tuple[Requirement, str]:
        """
        从用户输入中提取需求
        
        Args:
            user_input: 用户输入的自然语言
            current_requirement: 当前已有的需求（用于多轮对话）
            
        Returns:
            (提取的需求对象, 回复消息)
        """
        if not self.client:
            log_error("OpenAI客户端未初始化，无法提取需求")
            return Requirement(), "抱歉，系统配置有误，无法处理您的需求。"
        
        try:
            log_info("[Extractor] 开始提取需求，输入长度: %d", len(user_input))
            if current_requirement:
                log_info("[Extractor] 已有需求: %s", str(current_requirement.model_dump(exclude_none=True)))
            
            system_prompt = self._build_system_prompt()
            user_message = self._build_user_message(user_input, current_requirement)
            
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            messages.extend(self.conversation_history[-2:])
            messages.append({"role": "user", "content": user_message})
            
            log_info("[Extractor] 调用LLM，消息数: %d", len(messages))
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            log_info("[Extractor] LLM响应完成，使用token: %d", response.usage.total_tokens if hasattr(response, 'usage') else 0)
            
            result = json.loads(response.choices[0].message.content)
            
            requirement_dict = result.get("requirement", {})
            reply = result.get("reply", "")
            need_question = result.get("need_question", False)
            
            log_info("[Extractor] 提取到需求字段: %s", list(requirement_dict.keys()))
            
            if current_requirement:
                requirement = self._merge_requirement(current_requirement, requirement_dict)
                log_info("[Extractor] 合并需求完成")
            else:
                requirement = Requirement(**requirement_dict)
            
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": reply})
            
            if need_question and not requirement.is_complete():
                missing = requirement.get_missing_fields()
                if missing:
                    log_info("[Extractor] 需求不完整，缺失字段: %s", missing)
                    reply = self._generate_question(missing, requirement)
            
            log_info("[Extractor] 需求提取成功，完整性: %s，需求: %s", 
                     requirement.is_complete(), str(requirement.model_dump(exclude_none=True)))
            return requirement, reply
            
        except Exception as e:
            log_error("需求提取失败: %s", str(e))
            return Requirement(), "抱歉，我理解您的需求时遇到了问题，请重新描述一下您的租房需求。"
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词（优化版，减少token）"""
        return """提取租房需求，返回JSON：
{
    "requirement": {字段字典},
    "reply": "回复",
    "need_question": bool
}
字段：district,price_min,price_max,room_type,area_min,area_max,near_subway,has_elevator,water_electric,decoration,orientation,floor,lighting,move_in_date,commute_location
规则：只提取明确信息；聊天时need_question=false；缺少区域或预算时need_question=true"""
    
    def _build_user_message(self, user_input: str, current_requirement: Optional[Requirement] = None) -> str:
        """构建用户消息"""
        message = f"用户输入：{user_input}\n\n"
        if current_requirement:
            message += f"当前已有需求：{current_requirement.model_dump_json()}\n\n"
            message += "请更新需求信息，保留已有信息，只更新或新增用户提到的字段。"
        return message
    
    def _merge_requirement(self, current: Requirement, new_data: Dict[str, Any]) -> Requirement:
        """合并需求信息"""
        current_dict = current.model_dump(exclude_none=True)
        for key, value in new_data.items():
            if value is not None:
                current_dict[key] = value
        return Requirement(**current_dict)
    
    def _generate_question(self, missing_fields: list, requirement: Requirement) -> str:
        """生成追问消息"""
        if "区域" in missing_fields and "预算范围" in missing_fields:
            return "为了更好地为您推荐房源，请告诉我：\n1. 您想在哪个区域租房？（如：朝阳区、海淀区）\n2. 您的租金预算范围是多少？"
        elif "区域" in missing_fields:
            return "请告诉我您想在哪个区域租房？（如：朝阳区、海淀区）"
        elif "预算范围" in missing_fields:
            return "请告诉我您的租金预算范围是多少？"
        return "请补充一些关键信息，以便我为您推荐合适的房源。"
    
    def reset_conversation(self):
        """重置对话历史"""
        self.conversation_history = []