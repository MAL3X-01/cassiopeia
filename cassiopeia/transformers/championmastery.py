from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.championmastery import ChampionMasteryData, ChampionMasteryListData, ChampionMastery, ChampionMasteries
from ..dto.championmastery import ChampionMasteryDto, ChampionMasteryListDto

T = TypeVar("T")
F = TypeVar("F")


class ChampionMasteryTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Data

    @transform.register(ChampionMasteryDto, ChampionMasteryData)
    def champion_mastery_dto_to_data(self, value: ChampionMasteryDto, context: PipelineContext = None) -> ChampionMasteryData:
        data = deepcopy(value)
        return ChampionMasteryData(data)

    @transform.register(ChampionMasteryListDto, ChampionMasteryListData)
    def champion_mastery_list_dto_to_data(self, value: ChampionMasteryListDto, context: PipelineContext = None) -> ChampionMasteryListData:
        data = deepcopy(value)
        data["masteries"] = [self.champion_mastery_dto_to_data(c) for c in data["masteries"]]
        for c in data["masteries"]:
            c._update({"region": data["region"]})
        data = data["masteries"]
        return ChampionMasteryListData(data)

    # Core

    @transform.register(ChampionMasteryData, ChampionMastery)
    def champion_mastery_data_to_core(self, value: ChampionMasteryData, context: PipelineContext = None) -> ChampionMastery:
        return ChampionMastery(value)

    @transform.register(ChampionMasteryListData, ChampionMasteries)
    def champion_mastery_list_data_to_core(self, value: ChampionMasteryListData, context: PipelineContext = None) -> ChampionMasteries:
        return ChampionMasteries([self.champion_mastery_data_to_core(cm) for cm in value])
