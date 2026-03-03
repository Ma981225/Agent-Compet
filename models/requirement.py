"""
租房需求数据模型
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class Requirement(BaseModel):
    """租房需求模型"""
    district: Optional[str] = Field(None, description="区域，如：朝阳区、海淀区")
    price_min: Optional[float] = Field(None, description="最低租金预算")
    price_max: Optional[float] = Field(None, description="最高租金预算")
    room_type: Optional[str] = Field(None, description="户型，如：一居、两居、三居")
    area_min: Optional[float] = Field(None, description="最小面积（平方米）")
    area_max: Optional[float] = Field(None, description="最大面积（平方米）")
    near_subway: Optional[bool] = Field(None, description="是否要求近地铁")
    has_elevator: Optional[bool] = Field(None, description="是否要求有电梯")
    water_electric: Optional[str] = Field(None, description="水电类型，如：民水民电")
    decoration: Optional[str] = Field(None, description="装修情况，如：精装、简装")
    orientation: Optional[str] = Field(None, description="朝向，如：南、南北通透")
    floor: Optional[str] = Field(None, description="楼层要求")
    lighting: Optional[str] = Field(None, description="采光要求")
    move_in_date: Optional[str] = Field(None, description="入住时间")
    commute_location: Optional[str] = Field(None, description="通勤地点")
    
    def is_complete(self) -> bool:
        """判断需求是否完整（至少包含区域或价格范围）"""
        return bool(self.district or self.price_min or self.price_max)
    
    def get_missing_fields(self) -> List[str]:
        """获取缺失的关键字段"""
        missing = []
        if not self.district:
            missing.append("区域")
        if not self.price_min and not self.price_max:
            missing.append("预算范围")
        return missing
