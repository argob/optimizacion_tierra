##########################################################################################################
# Script realizado por Igal Kejsefman y Facundo Pesce                                                    #
# Trabajo completo en: https://www.argentina.gob.ar/produccion/cep/consejo-cambio-estructural/documentos #
##########################################################################################################

import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import LinearConstraint


# Leo el problema desde un csv
df_rinde = pd.read_csv("m_rend.csv", encoding='latin-1', sep=";")  # rinde por cultivo y provincia matriz A
#df_rinde = pd.read_csv("m_rend_pond.csv", encoding='latin-1', sep=";")  # rinde por cultivo y provincia matriz B

#df_min_prod = pd.read_csv("./min_prod.csv")  # produccion minima por cultivo
df_min_prod = pd.read_csv("./m_prod.csv", encoding='latin-1')  # produccion minima por cultivo

#df_max_land = pd.read_csv("./max_land.csv")  # Tierra disponible por provincia
df_max_land = pd.read_csv("./m_land_final.csv", encoding='latin-1', sep=";")  # Tierra disponible por provincia

df_frac_pobl = pd.read_csv("./m_pob.csv", encoding='latin-1')  # Fraccion poblacion x provincia

try:  # Leo solucion inicial si existe (area cultivada por cultivo x provincia)
    df_init_sol = pd.read_csv("./m_init_sol.csv", encoding='latin-1', sep=";")
except:
    df_init_sol = None


# armamos el vector beta
def uso_tierra(tierra_max, minima_prod, prop_pobla, rinde_ij):

    q_ij = []
    q_ij = pd.DataFrame(q_ij)

    for i_cult in range(0,len(minima_prod)):
        x = minima_prod.loc[i_cult, "min_prod"] * prop_pobla["frac_poblacion"]
        x = pd.DataFrame(x)
        q_ij = q_ij.append(x.T, ignore_index=True)

    rinde_ij = rinde_ij.drop(["Cultivo"], axis=1)
    rinde_ij = 1/ rinde_ij
    rinde_ij.columns = list(range(rinde_ij.shape[1]))
    rinde_ij.replace(np.inf, 0, inplace = True)

    denominador_j = q_ij.mul(rinde_ij)
    denominador_j = pd.DataFrame(denominador_j.sum())

    tierra_max_j = tierra_max.drop(["Provincia"], axis=1)

    tierra_max_j.columns = list(range(tierra_max_j.shape[1]))
    beta = tierra_max_j / denominador_j
    beta = pd.DataFrame(np.where(beta > 1, 1, beta))
    beta = beta.join(df_max_land["Provincia"])

    return  beta



# Paso a notacion matricial cultivo x provincia
rinde = df_rinde.drop(columns="Cultivo").values
min_prod = df_min_prod.drop(columns="Cultivo").values.transpose()[0]
max_land = df_max_land.drop(columns="Provincia").values.transpose()[0]
frac_pobl = df_frac_pobl.drop(columns="Provincia").values.transpose()[0]

init_sol = (
    np.zeros_like(rinde)
    if df_init_sol is None
    else df_init_sol.drop(columns="Cultivo").values
    )

df_max_uso_tierra = uso_tierra(df_max_land, df_min_prod, df_frac_pobl, df_rinde)
max_uso_tierra = df_max_uso_tierra.values.transpose()[0]


# El rinde me da las dimensiones del problema
n_cult, n_prov = rinde.shape

# Restricciones de la forma lb < a.dot(solución) < ub en notación matricial
# lb = lower bounds (límite inferior) 
# ub = upper bound (límite superior)
# a = restricción
a, lb, ub = [], [], []

# Agrego restricciones de producción minima por cultivo
for i_cult in range(n_cult):
    tmp = [0] * n_cult * n_prov
    tmp[i_cult * n_prov:(i_cult + 1) * n_prov] = rinde[i_cult]
    a.append(tmp)
    lb.append(min_prod[i_cult])
    ub.append(np.inf)

# Agrego restricciones de tierra maxima por provincia

for i_prov in range(n_prov):
    tmp = [0] * n_cult * n_prov
    for i_cult in range(n_cult):
        tmp[i_prov+n_prov*i_cult] = 1
    a.append(tmp)

#llegás a una matriz a así
#[[1,0,0,0,1,0,0,0,1,0,0,0],
# [0,1,0,0,0,1,0,0,0,1,0,0],
# [0,0,1,0,0,0,1,0,0,0,1,0],
# [0,0,0,1,0,0,0,1,0,0,0,1]]

#vectores de restricciones lb y ub
for i_prov in range(n_prov):
    lb.append(0)
    ub.append(max_land[i_prov])


# Agrego restricción: producción mínimia por cultivo por provincia según población
alpha = 1 # fracción de producción mínima proporcional a la población
for i_cult in range(n_cult):
    for i_prov in range(n_prov):
        if rinde[i_cult,i_prov]<=0: # No aplica restricción si algún rinde es 0
            continue
        else:
            tmp = [0] * n_cult * n_prov
            tmp[i_cult * n_prov + i_prov] = rinde[i_cult, i_prov]
            a.append(tmp)
            lb.append( (frac_pobl[i_prov] * min_prod[i_cult]) * max_uso_tierra[i_prov] * alpha)
            ub.append(np.inf)



a = [[float(x) for x  in sublist] for sublist in a]
lb = [float(x) for x  in lb]
ub = [float(x) for x  in ub]

constr = LinearConstraint(a, lb, ub)

# Optimización
def f(x):
    return x.sum()

res = minimize(
    f,
    init_sol.reshape(-1),
    bounds=[(0, np.inf) for _ in init_sol.reshape(-1)],
    constraints=constr, tol= 50,  method="SLSQP")

print(res.message)

# Resultado: matriz suelo utilizado por cultivo y provincia
cultivo_provincia = res.x.reshape((n_cult, n_prov))

df_cultivo_provincia = pd.DataFrame(cultivo_provincia, columns=df_rinde.columns.values[1:])
df_cultivo_provincia.insert(0, "Cultivo", df_rinde.Cultivo)

df_cultivo_provincia = pd.DataFrame(df_cultivo_provincia.round(0))

max_land_trasp = pd.pivot_table(data=df_max_land.rename(columns={"max_land":"Has. Disponibles"}), columns= "Provincia", values= "Has. Disponibles", index=None, aggfunc="sum").reset_index()

salida = pd.concat([df_cultivo_provincia,max_land_trasp], axis=0)

tierra_utilizada = cultivo_provincia.sum(axis=0).round()

proporción_utilizada = pd.DataFrame(tierra_utilizada/max_land*100)

proporción_utilizada = pd.concat([df_max_land.Provincia, proporción_utilizada], axis=1)

proporción_utilizada.columns = ["provincia", "proporción (%)"]

# Guardo solución como csv
proporción_utilizada.to_csv("propocion_tierras_a0.csv", index = False)
df_cultivo_provincia.to_csv("cultivo_provincia_a0.csv", index= False)



