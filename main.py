from fastapi import FastAPI, HTTPException



dictionnaire_de_couse = {
"farine": [200,"grammes"],
"oeuf": [6,"unité"]
}


app = FastAPI()

@app.get("/")
def index():
    """
    Retourne un message de bienvenue.
    """
    return {"message": "Bonjour bienvenue sur l’API liste de course"}


    
@app.get("/get_dictionnaire")
def get_dictionnaire():
    """
    Retourne le dictionnaire de course.
    """
    if len(dictionnaire_de_couse)== 0:
        return {"message": "Le dictionnaire est vide"}
    else:
        return {"content": dictionnaire_de_couse}



@app.post("/add_to_dictionnaire")
def add_to_dictionnaire(element: str, quantite:int, unite:None|str=None):
    # vérifier si l'element est déja dans le dictionnaire
    if element in dictionnaire_de_couse:
        if unite:
            # si il est dans le dictionnaire on vérifie que l'unité est la meme
            if unite == dictionnaire_de_couse[element][1]:
                # si l'unité est la memme, on ajoute les quantités
                dictionnaire_de_couse[element][0]+=quantite
                return {element:dictionnaire_de_couse[element]}
                # si l'unité est pas la meme, on renvoit un message d'erreur
            else:
                raise HTTPException(
                                    status_code=400, 
                                    detail=f"Not the good unit for element, {element} is in {dictionnaire_de_couse[element][1]} "
                                    )
        # pas d'unité fournie, j'ajoute par défault
        else:
            dictionnaire_de_couse[element][0]+=quantite
            return {element:dictionnaire_de_couse[element]}

    else:
        # si non, on ajoute l'element au dictionnaire
        dictionnaire_de_couse[element] = [quantite,unite]
        return {element:dictionnaire_de_couse[element]}
        
@app.delete("/remove_from_dictionnaire")
def remove_from_dictionnaire(element: str):
    if element in dictionnaire_de_couse:
        del dictionnaire_de_couse[element]
        return {"detail": f"{element} has been removed", "content": dictionnaire_de_couse}
    else:
        raise HTTPException(status_code=404, detail="Element not found in the dictionnaire")


# #  uvicorn main:app --reload