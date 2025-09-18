from fastapi import FastAPI,Request,Form,File,UploadFile,HTTPException,status
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import folium
from bancodedados import *
from pathlib import Path
import datetime
import shutil
import json

mundo_map = folium.Map(location=[-20,-20],zoom_start=2.5)
create_table()
templates=Jinja2Templates(directory="templates")
mundo_map.save("templates/mapa_mundi.html")
app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/",response_class=HTMLResponse)
def renderizar_mapa(request:Request):
    pontos = acessar_todos()
    for ponto in pontos:
        folium.Marker(
        location=[ponto[5], ponto[6]],
        popup=f"<img src={ponto[3]} style=\"width:7vw; height:auto\";/><b>{ponto[1]}</b><br>{ponto[2]}<br><b>criado em {ponto[4]}</b>",
        tooltip="Clique para mais info",
        icon=folium.Icon(color=ponto[7])
        ).add_to(mundo_map)
    mundo_map.save("templates/mapa_mundi.html")
    context={
        "request": request,  # OBRIGATÓRIO para Jinja2
        "nome": "Visitante",
        "data_hora": "16/09/2025",
        "usuario_logado": False
    }
    return templates.TemplateResponse("mapa_mundi.html",context)
@app.get("/add",response_class=HTMLResponse)
def abrir_formulario(request:Request):
    return templates.TemplateResponse("adicionar_pontos.html",{"request":request})
@app.post("/submeter_pontos",response_class=HTMLResponse)
def adicionar_pontos(request:Request,titulo:str=Form(...),texto:str=Form(...),cord_x:float=Form(...),cord_y:float=Form(...),imagem: UploadFile = File(...),cor:str=Form(...)):
    context={
        "request": request,  # OBRIGATÓRIO para Jinja2
        "nome": "Visitante",
        "data_hora": "16/09/2025",
        "usuario_logado": False
    }
    if not imagem.content_type.startswith("image/"):
        raise HTTPException(400, "Arquivo deve ser uma imagem")
    data_criacao=datetime.date.today()
    image=imagem.filename
    nome_arquivo=f'{data_criacao}_{image}'
    caminho_arquivo = f'static/images/{nome_arquivo}'
    Path("static/images").mkdir(parents=True, exist_ok=True)

    # Salvar o arquivo
    with open(caminho_arquivo, "wb") as buffer:
        shutil.copyfileobj(imagem.file, buffer)
    adicionar_item(titulo=titulo,texto=texto,imagem_path=caminho_arquivo,data_criacao=data_criacao,cord_x=cord_x,cord_y=cord_y,cor=cor)
        
    return RedirectResponse(url="/sucesso",status_code=303)
@app.get("/remove",response_class=HTMLResponse)
def mostrar_remocao(request:Request):
    items=transformar_em_json(acessar_todos())
    return templates.TemplateResponse("remover_pontos.html",{"request":request,"items":items})
@app.delete("/deletar")
def deletar(request:Request,id_item:int):
    deletar_item(id_item)
    return JSONResponse(content={"message":"removido com sucesso"},status_code=status.HTTP_200_OK)
@app.get("/sucesso",response_class=HTMLResponse)
def sucesso(request:Request,):
    return templates.TemplateResponse("sucesso.html",{"request":request})


