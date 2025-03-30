from pydantic import BaseModel, Field

class AnalysisItem(BaseModel):
    before: str = Field(description="Description of the state before the change")
    after: str = Field(description="Description of the state after the change")
    observation: str = Field(description="Objective observation about improvement or deterioration")

class Feedback(BaseModel):
    posture: AnalysisItem = Field(description="Analysis of posture changes")

    abdomen: AnalysisItem = Field(description="Analysis of abdomen changes")

    chest: AnalysisItem = Field(description="Analysis of chest changes")
    shoulders: AnalysisItem = Field(description="Analysis of shoulders changes")
    triceps: AnalysisItem = Field(description="Analysis of triceps changes")
    biceps: AnalysisItem = Field(description="Analysis of biceps changes")

    quads: AnalysisItem = Field(description="Analysis of quads changes")
    glutes: AnalysisItem = Field(description="Analysis of glutes changes, empty if there is no change or not visible.")
    calves: AnalysisItem = Field(description="Analysis of calves changes")
    hamstrings: AnalysisItem = Field(description="Analysis of hamstrings changes")

    back: AnalysisItem = Field(description="Analysis of back changes")

    general_observation: str = Field(description="General considerations about the evolution")
    body_fat_percentage: str = Field(description="Estimate of current body fat percentage, e.g.: '20%'")
