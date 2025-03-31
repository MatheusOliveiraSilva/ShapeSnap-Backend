from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from agent.shape_analyst.compare_shapes import ShapeAnalyst
import tempfile
import os

router = APIRouter()

class AnalysisResponse(BaseModel):
    feedback: dict
    message: str

class AnalysisRequest(BaseModel):
    language: Optional[str] = "English"

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_shapes(
    before_image: UploadFile = File(...),
    after_image: UploadFile = File(...),
    language: str = "English"
):
    """
    Analyze two images (before and after) to provide body composition feedback.
    
    Args:
        before_image: The 'before' image file
        after_image: The 'after' image file
        language: The language for the analysis output (default: English)
        
    Returns:
        AnalysisResponse containing the structured feedback
    """
    try:
        # Create temporary files to store the uploaded images
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(before_image.filename)[1]) as before_temp, \
             tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(after_image.filename)[1]) as after_temp:
            
            # Write uploaded files to temporary files
            before_content = await before_image.read()
            after_content = await after_image.read()
            
            before_temp.write(before_content)
            after_temp.write(after_content)
            
            # Initialize the shape analyst
            analyst = ShapeAnalyst()
            
            # Perform the analysis
            analysis = analyst.analyze_images(
                before_temp.name,
                after_temp.name,
                language=language
            )
            
            # Clean up temporary files
            os.unlink(before_temp.name)
            os.unlink(after_temp.name)
            
            return AnalysisResponse(
                feedback=analysis.dict(),
                message="Analysis completed successfully"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during analysis: {str(e)}"
        ) 