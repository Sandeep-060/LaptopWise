from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, ConfigDict, Field
from src.predictor import predict_price, compare_deal


# FastAPI Application
app = FastAPI(
    title="LaptopWise API",
    description="API for laptop price estimation and deal comparison.",
    version="1.0.0",
)


# Request Schemas
class LaptopInput(BaseModel):
    
    model_config = ConfigDict(extra="forbid")

    Brand: str
    Series: str
    Thickness: float
    Weight: float
    Operating_System: str = Field(alias="Operating System")
    Display_Size: float = Field(alias="Display Size")
    Display_Touchscreen: str = Field(alias="Display Touchscreen")
    Processor: str
    Graphic_Processor: str = Field(alias="Graphic Processor")
    RAM_Capacity_GB: float
    RAM_Type: str = Field(alias="RAM Type")
    SSD_Capacity: float = Field(alias="SSD Capacity")
    HDD_Capacity: float = Field(alias="HDD Capacity")
    Battery_Capacity: float = Field(alias="Battery Capacity")
    Fingerprint_scanner: str = Field(alias="Fingerprint scanner")


class DealInput(LaptopInput):
    asking_price: float

# Health Check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Price Prediction
@app.post("/predict")
def predict_laptop_price(laptop: LaptopInput):

    try:
        laptop_data = laptop.model_dump(by_alias=True)
        predicted_price = predict_price(laptop_data)
        return {"predicted_price": predicted_price}

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Model artifact not found."
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed."
        )

# Deal Comparison
@app.post("/compare")
def compare_laptop_deal(deal: DealInput):

    try:
        deal_data = deal.model_dump(by_alias=True)
        asking_price = deal_data.pop("asking_price")
        result = compare_deal(deal_data,asking_price)
        return result

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Model artifact not found."
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Comparison failed."
        )