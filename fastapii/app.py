from fastapi import FastAPI, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Quote
from schemas import QuoteCreate, Quote as QuoteSchema
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_quotes(request: Request, db: Session = Depends(get_db)):
    quotes = db.query(Quote).all()
    return templates.TemplateResponse("quote_list.html", {"request": request, "quotes": quotes})

@app.get("/add")
async def add_quote_form(request: Request):
    return templates.TemplateResponse("add_quote.html", {"request": request})

@app.post("/add")
async def add_quote(db: Session = Depends(get_db), text: str = Form(...), author: str = Form(...)):
    quote = Quote(text=text, author=author)
    db.add(quote)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/edit/{quote_id}")
async def edit_quote_form(request: Request, quote_id: int, db: Session = Depends(get_db)):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return templates.TemplateResponse("edit_quote.html", {"request": request, "quote": quote})

@app.post("/edit/{quote_id}")
async def edit_quote(quote_id: int, db: Session = Depends(get_db), text: str = Form(...), author: str = Form(...)):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    quote.text = text
    quote.author = author
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{quote_id}")
async def delete_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    db.delete(quote)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
