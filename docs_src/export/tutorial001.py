from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
import io

app = FastAPI()

data = [
	{"id": 1, "name": "Alice", "age": 25},
	{"id": 2, "name": "Bob", "age": 30},
]

@app.get("/export")
async def export_data(format: str = Query("json", enum=["json", "csv"])):
	df = pd.DataFrame(data)

	if format == "json":
    	return JSONResponse(content=df.to_dict(orient="records"))

	elif format == "csv":
    	output = io.StringIO()
    	df.to_csv(output, index=False)
    	output.seek(0)
    	return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=data.csv"})
