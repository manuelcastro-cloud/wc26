def repartir_bombo1_con_restricciones():
    if not bombo1:
        st.warning("Bombo 1 vacío")
        return
    
    # Asignaciones fijas
    fijas = {"México": "A", "Canadá": "B", "USA": "D"}
    for pais, grupo in fijas.items():
        # Buscar el objeto del país en el bombo
        obj = next((x for x in bombo1 if x["pais"] == pais), None)
        if obj:
            st.session_state.grupos[grupo][0] = obj["pais"]
            bombo1.remove(obj)
    
    # Países restantes
    paises_restantes = bombo1.copy()
    grupos_restantes = [letra for letra in st.session_state.grupos if letra not in fijas.values()]
    random.shuffle(paises_restantes)
    
    for i, letra in enumerate(grupos_restantes):
        if i < len(paises_restantes):
            st.session_state.grupos[letra][0] = paises_restantes[i]["pais"]
    bombo1.clear()
    st.success("Bombo 1 repartido con restricciones")
