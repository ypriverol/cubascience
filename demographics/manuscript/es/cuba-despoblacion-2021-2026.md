> **Generado automáticamente** desde `latex/main.tex` por `scripts/render_manuscript_md.py`. No editar a mano: los cambios se pierden.
> Versión maquetada (PDF): `Cuba_despoblacion_2021-2026_manuscrito.pdf`.
> Preprint; no revisado por pares. Código y datos: <https://github.com/ypriverol/cubascience> (`demographics/`).

# Auditoría de escenarios de la caída poblacional de Cuba, 2021–2026

Yasset Pérez-Riverol  
*Investigador independiente*  
`ypriverol@gmail.com`

Preprint · 3 de agosto de 2026  
Conjuntos de escenarios, una comprobación de consistencia con la mortalidad infantil,  
descomposición de la mortalidad atribuible y triangulación de registros independientes  
Versión en inglés y material suplementario, solo en inglés (esperanza de vida; provincias):  
`manuscript/en/cuba-depopulation-2021-2026-supplement.pdf`

## Resumen

**Antecedentes.** Cuba pierde población a uno de los ritmos más rápidos del hemisferio occidental en tiempos de paz. No se ha completado ningún censo desde 2012, y la Oficina Nacional de Estadística e Información (ONEI) retiró más de un millón de personas de su recuento publicado en una sola revisión de 2024. Los niveles publicados para fin de 2025 todavía abarcan de $`\sim`$<!-- -->8.0 a $`\sim`$<!-- -->11.0 millones. Este trabajo audita la caída del recuento 2021–2025 con conjuntos de escenarios transparentes, separa la migración del cambio demográfico interno, y reporta una continuación de escenario hasta fin de 2026.

**Métodos.** Resolvemos la identidad contable demográfica bajo tres escenarios —piso, central y superior—, cada uno especificado por tres números: la sobrestimación del padrón a fin de 2021, un multiplicador sobre la emigración neta de la ONEI, y el subregistro residual de defunciones. Las cifras puntuales son de forma cerrada y exactas por linealidad; un Monte Carlo reducido reporta únicamente rangos de sensibilidad a los supuestos. Ningún parámetro se informa con una verosimilitud, de modo que son valores de escenario, no estimaciones, y los rangos no son intervalos de confianza. Todos los resultados se enuncian sobre una sola base: el stock oficial de fin de 2021. Los registros externos se usan como techos o corroboración blanda; el escenario central nunca se trata como validación externa de sí mismo. Por separado, descomponemos el cambio en las defunciones anuales desde 2019 mediante estandarización indirecta por edad sobre la mortalidad por edades de la ONEI, separándolo en un término de tamaño poblacional, un término de envejecimiento y un término residual de tasas reportado como exceso de defunciones respecto de la tabla de tasas por edad de 2019.

**Resultados.** Frente al stock oficial de fin de 2021 (11.11 millones), la brecha a fin de 2025 abarca **1.97–2.79 millones** (**17.8–25.1%**) entre tres conjuntos de supuestos; un escenario nulo que toma a la ONEI al pie de la letra da 1.68 millones (exactamente, por construcción) y se reporta junto a ellos. Hay que separar dos cantidades. Frente al *stock oficial de 2021*, la brecha del escenario central es de **2.53 millones** (22.8%), pero 1.68 millones de eso es caída que la propia ONEI publicó, de modo que solo **0.85 millones** es la corrección añadida por este trabajo. Frente a la cifra de la ONEI para *fin de 2025* (9.43 millones), la población viva del escenario central (**8.58 millones**) es menor en **0.85 millones**. Esos 0.85 millones son la afirmación real del trabajo; los 2.53 millones son la suma de ambas. Un escenario nulo ($`U_0{=}0`$, $`M{=}1`$, $`D_{\mathrm{fac}}{=}1`$) reproduce exactamente la cifra publicada por la ONEI y se reporta junto a los tres conjuntos de supuestos. Alrededor del **92%** de esa brecha es emigración, contando tanto el flujo de 2022–2025 como el rezago previo a 2021 que sigue en el padrón. La continuación a fin de 2026 sitúa el escenario central cerca de **8.29 millones**. Cuba registró 27 100 defunciones más en 2025 que en 2019, o unas 31 300 una vez añadidas las defunciones no registradas estimadas, mientras que el stock del escenario central es unos 2 millones menor. La estandarización por edad separa dos fuerzas al alza de magnitud comparable —unas **22 400** defunciones adicionales al año por una población más envejecida y unas **28 500** al año (rango de sensibilidad a los supuestos: 18 600–38 200) de exceso respecto de la tabla de 2019— frente a unas 19 400 defunciones menos al año por la menor población. Excluyendo la ola pandémica de 2021, el total de exceso en 2022–2025 es de $`\sim`$**74 900** (47 000–103 100), condicionado a un ancla plana de 2019; la elección del contrafactual lo mueve entre 45 200 y 103 300, una incertidumbre de tamaño comparable, ortogonal a ese rango. Tampoco domina ningún término interno de la simulación: congelando cada uno por turno, la proyección por cohortes explica en torno a un cuarto de la amplitud de la banda y el resto menos.

**Conclusiones.** La despoblación es predominantemente migratoria en el recuento, reforzada por el desplome de los nacimientos, la mortalidad elevada y el envejecimiento acelerado. Frente al stock oficial de 2021, la brecha hacia fin de 2026 se acerca a una de cada cuatro personas; al usarse una sola base, es la misma cantidad que el titular y no una definición distinta. La mortalidad es una fracción pequeña de la pérdida de recuento pero un costo humano grande: es medible por separado, aproximadamente la mitad no se explica por el envejecimiento, y sigue creciendo.

**Palabras clave:** Cuba; demografía; emigración; decrecimiento natural; mortalidad infantil; fecundidad; envejecimiento; calidad de los datos estadísticos.

# Introducción

Contar cubanos se ha vuelto un asunto en disputa. El último censo completado fue el de 2012; el censo previsto para 2022 se ha pospuesto repetidamente y ahora se promete para 2026 (ONEI 2022). Sin censo, la población publicada depende de proyecciones y de un registro migratorio rezagado (Preston et al. 2001; United Nations, Department of Economic and Social Affairs, Population Division 2024). En julio de 2024 la ONEI informó una “población efectiva” de 10 055 968 a fin de 2023 (cerca de un millón por debajo de los niveles publicados previamente), luego 9 748 007 (fin de 2024) y 9 434 593 (fin de 2025) (ONEI 2024, 2025).

Coexisten tres series incompatibles (Figura <a href="#fig:pop" data-reference-type="ref" data-reference="fig:pop">7</a>): la trayectoria de *World Population Prospects* de Naciones Unidas, cercana a 10.9 millones (que todavía supone una emigración neta del orden de $`2\times10^4`$ al año) (United Nations, Department of Economic and Social Affairs, Population Division 2024; Economic Commission for Latin America and the Caribbean (ECLAC) 2022); la serie oficial revisada de la ONEI (9.43 millones a fin de 2025); y estudios independientes que sitúan la población viva más cerca de 8.0–8.6 millones (Albizu-Campos Espiñeira 2023, 2024). Casi tres millones de personas separan los extremos. Este trabajo presenta una auditoría de escenarios de la caída del recuento 2021–2025 con conjuntos de distribuciones a priori transparentes, separa los componentes migratorio e interno, compara la contabilidad migratoria oficial con los registros de los países de destino, y reporta una continuación de escenario a fin de 2026.

La transición de la fecundidad cubana fue de las más tempranas y profundas de América Latina (Díaz-Briquets and Pérez 1982; Hollerbach et al. 1984; Díaz-Briquets 2014), de modo que una fecundidad por debajo del reemplazo no es novedad. Lo nuevo es la *velocidad* de la pérdida de recuento bajo emigración y decrecimiento natural combinados, en un contexto regional donde América Latina y el Caribe todavía crecen en conjunto (Economic Commission for Latin America and the Caribbean (ECLAC) 2022; United Nations, Department of Economic and Social Affairs, Population Division 2024). Contracciones comparables en tiempos de paz en otros países han estado impulsadas sobre todo por la emigración (por ejemplo, Venezuela) (Coleman 2006; García et al. 2019).

**Tesis central.** La pérdida de recuento es mayoritariamente emigración, pero un segundo motor “interno” (caída de nacimientos, exceso de mortalidad y envejecimiento) sostendría la contracción incluso si la emigración se frenara (Lee and Mason 2014; Lesthaeghe 2010). Los dos motores no son independientes: la salida selectiva de adultos en edad laboral y de mujeres en edad reproductiva causa buena parte de la caída de la fecundidad, de modo que muchos “nacimientos que no ocurren” son un efecto migratorio diferido (Bongaarts and Sobotka 2012; Díaz-Briquets 2014).

# Métodos

La ecuación de balance es la identidad contable demográfica estándar (Preston et al. 2001). Los agregados registrados por la ONEI para 2022–2025 son anclas fijas (ONEI 2025). Su procedencia es desigual: los recuentos vitales de 2019–2022 están en los cuadros de la ONEI que distribuimos, las defunciones de 2023 quedan corroboradas de forma independiente por la submisión cubana a la OMS, pero los nacimientos y defunciones de 2024 (71 374 y 128 098) no aparecen en ningún cuadro a nuestro alcance y descansan en el reporte estatal. El total de defunciones de 2024 alimenta la cifra de exceso de ese año y todas las ventanas acumuladas, y es el eslabón más débil de la serie. nacimientos $`B^{\mathrm{reg}}=325\,233`$, defunciones $`D^{\mathrm{reg}}=502\,149`$, y emigración neta consistente con la identidad $`R=1\,501\,706`$. La población oficial a fin de 2021 es $`P^{\mathrm{off}}_{2021}=11\,113\,215`$. Cada extracción Monte Carlo muestrea correcciones latentes y aplica
``` math
\begin{align}
P_{2021} &= P^{\mathrm{off}}_{2021} - U_0, \\
D &= D^{\mathrm{reg}}\,D_{\mathrm{fac}} \;\;(+\;\text{pulso epidémico opcional en B/C}), \\
M_{\mathrm{net}} &= R\,M, \\
\Delta &= (D - B) + M_{\mathrm{net}}, \\
P_{2025} &= P_{2021} - \Delta,
\end{align}
```
donde $`U_0`$ es la sobrestimación de base a fin de 2021 (personas ya efectivamente en el exterior pero aún en el padrón), $`M\ge 1`$ escala la emigración neta de la ONEI, y $`D_{\mathrm{fac}}\ge 1`$ escala las defunciones registradas. La pérdida se reporta sobre una sola base: el stock *oficial* de fin de 2021. La brecha que define tiene tres partes aditivas —sobrestimación de base $`U_0`$, emigración neta $`R\,M`$ y decrecimiento natural—, de modo que no hace falta un segundo porcentaje sobre “base corregida”.

Cada escenario son tres números, y la cifra puntual es la aritmética anterior evaluada en sus medias a priori, exacta porque la identidad es lineal en las tres. Verificamos que eso era todo lo que hacía la simulación: un Monte Carlo de $`10^6`$ extracciones con cópula gaussiana sobre las mismas marginales coincide con la forma cerrada dentro de unos cientos de personas (1 117 en el escenario superior), es decir, dentro del ruido de muestreo. Por eso la cópula se ha eliminado: movía la mediana unas 2 200 personas y solo ensanchaba una banda interna que no es nuestro enunciado primario de incertidumbre. Se conserva un muestreo reducido ($`N=2\times10^5`$, marginales independientes) únicamente para reportar esa banda, que sigue siendo una dispersión *predictiva a priori* y no error muestral. La **envolvente entre escenarios** es el enunciado primario (Pérez-Riverol 2026a, 2026b).

Definimos tres escenarios y cada uno se gana su lugar. El **conservador** añade una corrección modesta. *No* es una cota inferior consistente con la ONEI: su $`M`$ medio es 1.089, un 9% más de emigración que la reportada. El caso de corrección cero es el escenario nulo. El **central** eleva el prior migratorio por encima de la ONEI y acota el subregistro de defunciones al 9%, apenas por encima del 7.5% que el propio registro perdió en 2022 sin explicación. El **superior** define el techo de la envolvente. Versiones anteriores llevaban cinco conjuntos de priores; dos se han retirado. Una variante ajustada por crisis quedaba a 0.02 millones del escenario central —el mismo escenario con otros diales— y un acompañante de reconstrucción vital basado en un índice ponderado a mano ha sido superado por la descomposición de mortalidad atribuible, que estima la misma cantidad a partir de datos por edad observados y no de una puntuación adimensional. Son **escenarios** (narrativas a priori), no estimadores identificados de una población viva única. Las revisiones de la ONEI de 2023–2024 ya absorbieron un stock rezagado grande, de modo que escalar el $`R`$ revisado por $`M>1`$ *y* restar un $`U_0`$ grande puede contar dos veces el mismo defecto; por eso reportamos siempre el piso junto al central.

<div id="tab:priors">

| Símbolo | Marginal | Interpretación |
|:---|:---|:---|
| $`U_0`$ | $`700\,000\times\mathrm{Beta}(2.0,2.4)`$ | Sobrestimación del padrón a fin de 2021 |
| $`M`$ | $`1+0.72\times\mathrm{Beta}(2.2,2.4)`$ | Multiplicador sobre la emigración neta ONEI $`R`$ |
| $`D_{\mathrm{fac}}`$ | $`1+0.09\times\mathrm{Beta}(1.8,3.2)`$ | Subregistro residual de defunciones (canal de ancianos en el domicilio) |

Especificación de distribuciones a priori del escenario central (tres marginales; sin estructura de dependencia). La cifra puntual usa las medias a priori de estas tres marginales. Escalas Beta: $`U_0\in[0,700\,000]`$, $`M\in[1,1.72]`$, $`D_{\mathrm{fac}}\in[1,1.09]`$. Ruido de nacimientos independiente $`B=B^{\mathrm{reg}}\mathcal{N}(1,0.01^2)`$.

</div>

La mortalidad infantil subió de 5.0 a 9.9 por mil nacidos vivos (2019–2025), un incremento del $`\sim`$<!-- -->98% en la *tasa*. El valor de 2025 es una cifra reportada y no está en ningún cuadro de la ONEI a nuestro alcance. La mayor parte es el denominador: las defunciones infantiles pasaron de 552 (observado, ONEI 3.16) a $`\sim`$<!-- -->674 (derivado), un 22%, mientras los nacidos vivos caían un 38%. Ambas cifras importan y reportar solo la tasa sobrestima la señal. Las defunciones infantiles son comparativamente difíciles de ocultar, de modo que la tasa infantil suele tratarse como un centinela de alta integridad del *estrés* del sistema de salud. Dos advertencias lo matizan: el valor de 2025 procede de prensa y no está en los cuadros de la ONEI a nuestro alcance, y existe literatura que cuestiona la clasificación fetal tardía y neonatal precoz en el margen de viabilidad en Cuba (Berdine et al. 2018), de modo que parte de cualquier alza puede ser relajación de la práctica de clasificación y no deterioro. En el mismo período la tasa bruta de mortalidad registrada subió de 9.7 a 14.2 por mil ($`\sim`$<!-- -->46%). Ambas se movieron con fuerza al alza a la vez, que es el aspecto de un sistema que se deteriora con un registro de defunciones intacto; un registro que ocultara muertes a gran escala mostraría el centinela subiendo mientras la mortalidad general se mantiene plana. Versiones anteriores convertían esto en una elasticidad logarítmica calibrada con Venezuela. Ese paso se ha eliminado: descansaba en dos números de un solo país sin incertidumbre asociada, y la conclusión —no hay firma de ocultamiento a gran escala— se sigue del comovimiento sin él. El subregistro residual en el escenario central queda limitado a un canal pequeño de ancianos fallecidos en el domicilio (central $`\sim`$<!-- -->3%, tope 9%) (Pérez-Riverol 2026b).

La mortalidad se trata como un estimando separado del recuento, y la pregunta que responde también es distinta: ¿cuántos cubanos están muriendo porque el sistema de salud se ha deteriorado, y no porque la población residente es más vieja? Una línea base de tasa bruta no puede responderla, porque carga a la crisis todo el desplazamiento etario, del 20.4% de 60 años y más en 2019 a aproximadamente 25–27% en 2025. Por eso reemplazamos el puente basado en tasas brutas usado en versiones anteriores de este trabajo por una estandarización indirecta por edad (Preston et al. 2001).

Sea $`m^{2019}_a`$ la tasa de mortalidad por edad en 2019 tomada del cuadro 3.15 de la ONEI, sobre los grupos $`a\in\{0\text{--}14,\,15\text{--}59,\,60\text{--}64,\,65+\}`$: el conjunto más fino que el cuadro de defunciones comparte con el cuadro 3.3 de la ONEI, que publica anualmente la población media por edades. Separar el grupo de 60 y más importa: la cohorte nacida en los años sesenta está entrando ahora a los 60–64, de modo que el grupo de mayores se está volviendo *más joven* (60–64 pasó del 25.7% de la población de 60 y más en 2019 al 27.9% en 2022), y un único grupo abierto de 60 y más leería ese cambio de composición como un alza de la mortalidad. Las defunciones esperadas en el año $`t`$ bajo un sistema de salud inalterado de 2019 son $`E_t=\sum_a m^{2019}_a P_{a,t}`$, y el cambio en las defunciones anuales desde 2019 se descompone exactamente en
``` math
\begin{align}
\text{tamaño} &= (P_t-P_{2019})\,\mathrm{TBM}_{2019}/1000, \\
\text{envejecimiento} &= \textstyle\sum_a m^{2019}_a (P_{a,t}-P_{a,2019})/1000 - \text{tamaño}, \\
\text{tasas} &= D_t\,D_{\mathrm{fac}} - E_t,
\end{align}
```
con $`D_t D_{\mathrm{fac}} - D_{2019} = \text{tamaño}+\text{envejecimiento}+\text{tasas}`$. Es una descomposición de tipo Kitagawa aplicada a un *conteo* de defunciones y no a una diferencia de tasas brutas; el término de tamaño es el análogo, en conteos, de mantener fija la exposición (Kitagawa 1955). El término de tasas es el *exceso de defunciones respecto de la tabla de tasas por edad de 2019*. Deliberadamente no lo llamamos “atribuible al deterioro del sistema de salud”. La misma fórmula aplicada a 2021 devuelve $`\sim`$<!-- -->61 900, que es una pandemia y no un sistema de salud; un residual contra una tabla fija absorbe la mortalidad pandémica y pos-aguda, la deriva de codificación, el desplazamiento de mortalidad, la emigración selectiva por salud y el error de denominador sin distinguir entre ellos. Atribuir exigiría una exposición identificada, evidencia de causa de muerte compatible con el mecanismo, y la exclusión cuantitativa de las alternativas: nada de lo cual tenemos.

La descomposición es mucho menos sensible al denominador que el puente basado en tasas brutas al que sustituye. En 2019, el 82% de las defunciones cubanas ocurrieron a los 60 años o más, mientras que la emigración es $`\sim`$<!-- -->77% de 15 a 59 años. Por eso mantenemos aproximadamente fijo el *número* de ancianos entre escenarios de población, de modo que bajo el escenario central las mismas personas mayores quedan sobre un total menor y la proporción de 60 y más sube a $`\sim`$<!-- -->29% (frente a $`\sim`$<!-- -->26% oficial). Ese $`\sim`$<!-- -->29% es un supuesto de esta descomposición, no una observación. Una versión anterior lo describía como conservador con el argumento de que el número de ancianos se mantiene fijo; eso era erróneo en el hecho y en la dirección. La proyección *no* mantiene fijo el número —retira emigrantes mayores según la proporción del 8%— y hacerlo *eleva* el resultado: con una proporción del 0% (número genuinamente fijo) el exceso de 2025 es 23 700 y el total 2022–2025 62 800, frente a 28 500 y 74 900 tal como se usa, y con el 16% son 33 300 y 86 900. Esa única distribución a priori experta mueve por tanto el titular en $`\pm`$<!-- -->4 800 al año y $`\pm`$<!-- -->12 000 acumulados: en torno a un cuarto y un quinto de los respectivos rangos de sensibilidad. Su consecuencia es que $`E_t`$ apenas cambia entre la población oficial ($`\sim`$<!-- -->9.4 M) y la del escenario central ($`\sim`$<!-- -->8.6 M), mientras que una tasa bruta aplicada a la población menor infla mecánicamente el residual. La estructura por edades es *observada* para 2019–2022 y se proyecta por cohortes para 2023–2026 a partir de la estructura observada de 2022, con entradas desde la cohorte de 55–59, salidas a la tabla de tasas de 2019, y emigración de mayores según la proporción del 8% de emigrantes de 60 y más. Dos elecciones de la proyección empujan el resultado a la baja y dos al alza, y ambas direcciones deben declararse. A la baja: las edades 40–59 no reciben mermas por emigración ni mortalidad, y $`U_0`$ no se retira de la estructura de 2022, lo que infla el stock de mayores proyectado y reduce el exceso en torno a 1 000 defunciones en 2025. Al alza: la proporción del 8% de mayores se aplica a la cifra de migración neta de 2023 de 1 006 000, que este mismo trabajo argumenta que es una puesta al día del registro y no un flujo —lo que retira $`\sim`$<!-- -->80 000 mayores en un año y eleva el resultado de 2025 en unas 2 450— y el reparto 35/65 de los emigrantes mayores entre 60–64 y 65 y más se sitúa en el extremo de su rango plausible que maximiza el exceso (un reparto 50/50 baja 2025 en $`\sim`$<!-- -->750). No hemos reconciliado el tratamiento de 2023 con el argumento de la puesta al día del registro y lo señalamos como una inconsistencia. Nunca derivamos el número de mayores como (proporción por edad $`\times`$ total oficial): el total oficial absorbe en un solo salto la puesta al día del registro de la ONEI en 2023, y multiplicar ese salto por una proporción etaria elimina residentes mayores que nunca emigraron. Propagamos cuatro fuentes de incertidumbre sobre $`N=2\times10^5`$ extracciones: ruido del 2% sobre la tabla de tasas por edad de 2019; una deriva residual simétrica $`\mathcal{N}(0,0.03)`$ para la composición dentro del grupo de 65 y más después de 2022; la distribución a priori de $`D_{\mathrm{fac}}`$ del escenario central para defunciones no registradas; y una mezcla 50/50 entre la trayectoria poblacional oficial y la del escenario central, con un error de proyección que crece 1.5% por año más allá de 2022. Los parámetros sistemáticos se extraen una sola vez y se reutilizan en cada año, de modo que las ventanas acumuladas propagan error correlacionado y no independiente. La identidad anterior se cumple exactamente en cada extracción porque la referencia de 2019 usa las mismas tasas perturbadas que el año objetivo. Dado que $`D_{\mathrm{fac}}`$ es compartido con el escenario central, la estimación de exceso y el escenario de recuento no son independientes. Debe declararse una elección más: $`D_{\mathrm{fac}}`$ eleva los años objetivo pero no el ancla de 2019, de modo que entra como un *deterioro de la completitud del registro desde 2019* y no como un nivel constante. Esa es la lectura que pretendemos —un canal de ancianos fallecidos en el domicilio inducido por la crisis, inexistente en 2019, genera exceso real— pero eleva el resultado. Aplicar $`D_{\mathrm{fac}}`$ simétricamente al ancla da 24 900 para 2025 y 60 600 para 2022–2025, un 13% y un 18% por debajo del titular. Versiones anteriores llevaban además un comparador de exceso bruto registrado sobre un contrafactual de deriva lineal. Se ha eliminado: no se reproducía a partir de la fórmula declarada, su deriva quedaba por debajo de la deriva bruta precrisis observada en Cuba, y no servía a ningún argumento que la descomposición estandarizada por edad no sirva mejor (Karlinsky and Kobak 2021; Msemburi et al. 2023; Kishore et al. 2018).

Los niveles de población publicados se agrupan por contenido informativo (Figura <a href="#fig:tri" data-reference-type="ref" data-reference="fig:tri">6</a>). Los techos que no depuran emigrantes incluyen *World Population Prospects* de la ONU, el denominador del MINSAP y el padrón electoral (solo cotas superiores blandas). El recuento oficial revisado de la ONEI es 9.43 M a fin de 2025. Las construcciones independientes o que corrigen por salida incluyen viviendas$`\times`$ocupación ($`\sim`$<!-- -->8.7 M; escalar de ocupación frágil) y Albizu-Campos 2023/2024 (8.0–8.6 M; métodos que comparten con este trabajo los supuestos de crítica migratoria). El escenario central (8.58 M) es el estimando del estudio y *no* es validación externa de sí mismo; la coincidencia con Albizu o con viviendas es en parte un eco de distribuciones a priori compartidas, mientras que los techos acotan por arriba. La banda blanda de las fuentes que corrigen por salida está cerca de 8.0–8.9 millones.

El piso de destinos bajo concepto de asentamiento (Cuadro <a href="#tab:bridge" data-reference-type="ref" data-reference="tab:bridge">2</a>) comprende Estados Unidos $`\sim`$<!-- -->800 000 (estatus administrativos / flujo CBP, *no* el stock de la ACS), total no estadounidense $`\sim`$<!-- -->250 000 (España $`\sim`$<!-- -->135 000 + Uruguay $`\sim`$<!-- -->35 000 + resto $`\sim`$<!-- -->80 000), y un piso de $`\sim`$<!-- -->1.05 millones (Pérez-Riverol 2026d; Moslimani and Passel 2024). El stock de nacidos en Cuba de la ACS creció solo $`\sim`$<!-- -->335 000 entre 2019 y 2024, un piso menor de cambio de stock que no debe igualarse en silencio con la cifra administrativa de 800 000. Los conteos de encuentros y las solicitudes de nacionalidad son conceptos distintos y nunca se suman al piso de asentados (U.S. Customs and Border Protection 2024).

<div id="tab:bridge">

| Concepto | Conteo aprox. | Papel |
|:---|---:|:---|
| Piso de destinos asentados (admin. EE.UU. + no EE.UU.) | 1.05 M | Cota inferior (concepto asentados) |
| Alza del stock ACS de nacidos en Cuba 2019–24 (no asentados) | $`\sim`$<!-- -->0.34 M | Piso de cambio de stock; no sumar |
| Brecha no cuantificada hacia $`R`$ de la ONEI | $`\to\sim`$<!-- -->1.5 M | Residual, no personas validadas |
| Neto $`R`$ ONEI consistente con la identidad (2022–25) | 1.50 M | Flujo oficial tras la revisión |
| Neto tipo Albizu-Campos | $`\sim`$<!-- -->1.8 M | Narrativa superior independiente |
| Mediana $`R\times M`$ del escenario central | $`\sim`$<!-- -->2.0 M | Motor de escenario impulsado por distribuciones a priori |
| Encuentros en EE.UU. 2022–2024 (no asentados) | $`\sim`$<!-- -->0.85 M | Eventos; no sumar al piso |
| Solicitudes de nacionalidad española | $`\sim`$<!-- -->0.30 M | Muchos solicitantes siguen en Cuba |

Puente desde el piso de destinos asentados hacia los motores migratorios de los escenarios. Solo el piso tiene carácter de libro mayor; las filas posteriores son residuales o distribuciones a priori, no microdatos de destino.

</div>

Los datos de destino *no* identifican los $`\sim`$<!-- -->2.0 millones de emigración neta del escenario central; sostienen un piso grande y dejan la trayectoria de 1.05 a 2.0 como relleno blando de brecha más una distribución a priori migratoria. Si la emigración neta verdadera estuviera más cerca de 1.5 que de 2.0 millones, la población viva se situaría hacia $`\sim`$<!-- -->9.1 en lugar de $`\sim`$<!-- -->8.6 millones; la pérdida acumulada seguiría siendo grande y la emigración seguiría dominando la pérdida absoluta en todos los escenarios del Cuadro <a href="#tab:models" data-reference-type="ref" data-reference="tab:models">4</a>. Condicionada a las extracciones de fin de 2025, la continuación de escenario a fin de 2026 usa nacimientos centrados en 65 682 (ruido $`\mathcal{N}`$ del 3%), defunciones centradas en $`1.04\times 136\,214`$ multiplicadas por el mismo $`D_{\mathrm{fac}}`$, y una mezcla de tres regímenes de emigración neta con probabilidades $`(0.35,0.35,0.30)`$ sobre centros $`(150\,000,\;210\,000,\;300\,000)`$ más ruido del 15% en escala logarítmica. El alza del $`\sim`$<!-- -->4% en defunciones y los pesos de los regímenes son supuestos de escenario, no un pronóstico validado. Las trayectorias hacia $`\sim`$<!-- -->7 millones en 2030 de la Figura <a href="#fig:pop" data-reference-type="ref" data-reference="fig:pop">7</a> son **escenarios de tendencia ilustrativos** (visualmente, el tramo posterior a 2026); no son pronósticos probabilísticos.

# Resultados

<div id="tab:headline">

<table>
<caption>Cantidades principales por afirmación. Las bandas son predictivas a priori al 90% bajo las marginales indicadas, no error muestral. “Escenario” marca una cantidad que depende de un supuesto y no de una observación.</caption>
<thead>
<tr>
<th style="text-align: left;">Afirmación</th>
<th style="text-align: left;">Cantidad</th>
<th style="text-align: right;">Valor</th>
<th style="text-align: left;">Estatus</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4" style="text-align: left;"><em>Migración</em></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Piso de destinos asentados, documentado</td>
<td style="text-align: right;">1.05 M</td>
<td style="text-align: left;">cota inferior</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Neto ONEI consistente con la identidad, 2022–25</td>
<td style="text-align: right;">1.50 M</td>
<td style="text-align: left;">oficial</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Motor migratorio del escenario central</td>
<td style="text-align: right;"><span class="math inline">∼</span>2.0 M</td>
<td style="text-align: left;">a priori</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Participación de la emigración en el flujo 2022–25 (central)</td>
<td style="text-align: right;"><span class="math inline">∼</span>91%</td>
<td style="text-align: left;">escenario</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Saldo migratorio declarado ONEI, 2021 / 2022</td>
<td style="text-align: right;"><span class="math inline">+</span>169 / <span class="math inline">+</span>991</td>
<td style="text-align: left;">oficial</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Llegadas de cubanos registradas en EE.UU., 2021 / 2022</td>
<td style="text-align: right;">54 818 / 313 506</td>
<td style="text-align: left;">externo</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Fallos de consistencia de severidad alta</td>
<td style="text-align: right;">7 de 18</td>
<td style="text-align: left;">auditoría</td>
</tr>
<tr>
<td colspan="4" style="text-align: left;"><em>Deterioro del sistema de salud</em></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Defunciones registradas, 2025</td>
<td style="text-align: right;">136 214</td>
<td style="text-align: left;">oficial</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Esperadas a tasas de 2019, estructura de 2025</td>
<td style="text-align: right;">112 100</td>
<td style="text-align: left;">derivado</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Exceso vs la tabla de 2019, 2025</td>
<td style="text-align: right;">28 500 [18 600–38 200]</td>
<td style="text-align: left;">valor de escenario</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Exceso, 2022–2025 (pospandémico)</td>
<td style="text-align: right;">74 900 [47 000–103 000]</td>
<td style="text-align: left;">valor de escenario</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">bajo contrafactuales alternativos</td>
<td style="text-align: right;">45 200–103 300</td>
<td style="text-align: left;">sensibilidad</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">sobre el total de 2022 previo a la revisión</td>
<td style="text-align: right;"><span class="math inline">∼</span>84 100</td>
<td style="text-align: left;">sensibilidad</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Explicadas solo por el envejecimiento, 2025</td>
<td style="text-align: right;">22 400</td>
<td style="text-align: left;">derivado</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Efecto del tamaño poblacional, 2025</td>
<td style="text-align: right;"><span class="math inline">−</span>19 400</td>
<td style="text-align: left;">derivado</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Razón de mortalidad estandarizada vs 2019, 2025</td>
<td style="text-align: right;">1.215</td>
<td style="text-align: left;">derivado</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Parte de la tasa bruta que es estructura por edad (2019)</td>
<td style="text-align: right;">40.8%</td>
<td style="text-align: left;">derivado</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Retiro documentado del registro en 2022</td>
<td style="text-align: right;">8 951 (7.5%)</td>
<td style="text-align: left;">oficial</td>
</tr>
<tr>
<td colspan="4" style="text-align: left;"><em>Población proyectada</em></td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Brecha vs oficial 2021, entre conjuntos de supuestos</td>
<td style="text-align: right;">1.97–2.79 M</td>
<td style="text-align: left;">rango de escenarios</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">de la cual, caída ya publicada por la ONEI</td>
<td style="text-align: right;">1.68 M</td>
<td style="text-align: left;">oficial</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">corrección añadida por este trabajo (central)</td>
<td style="text-align: right;">0.85 M</td>
<td style="text-align: left;">valor de escenario</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Población viva fin-2025 (central)</td>
<td style="text-align: right;">8.58 M</td>
<td style="text-align: left;">escenario</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Brecha, escenario central</td>
<td style="text-align: right;">2.53 M (22.8%)</td>
<td style="text-align: left;">escenario</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Cifra oficial ONEI fin-2025</td>
<td style="text-align: right;">9.43 M</td>
<td style="text-align: left;">oficial</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Población viva fin-2026 (central)</td>
<td style="text-align: right;">8.29 M</td>
<td style="text-align: left;">escenario</td>
</tr>
<tr>
<td style="text-align: left;"></td>
<td style="text-align: left;">Participación de la emigración en la brecha</td>
<td style="text-align: right;"><span class="math inline">∼</span>92%</td>
<td style="text-align: left;">escenario</td>
</tr>
</tbody>
</table>

</div>

## Migración

El Cuadro <a href="#tab:bridge" data-reference-type="ref" data-reference="tab:bridge">2</a> separa los conteos de asentados de los encuentros, del cambio de stock de la ACS y de las solicitudes de nacionalidad. El piso de asentados ($`\sim`$<!-- -->1.05 M) confirma que la emigración es grande sin dejar de ser una cota inferior. Cerrar la brecha hacia los $`\sim`$<!-- -->1.5 millones de la ONEI es un residual no cuantificado; los $`\sim`$<!-- -->2.0 millones del escenario central son una distribución a priori sobre $`R`$, no una identificación por destinos. Si el neto verdadero está más cerca de 1.5 que de 2.0 millones, la población viva se sitúa hacia el extremo alto de nuestra banda ($`\sim`$<!-- -->9.1 en lugar de 8.6 M). La emigración sigue dominando la pérdida absoluta en todos los escenarios del Cuadro <a href="#tab:models" data-reference-type="ref" data-reference="tab:models">4</a>.

Los propios números de la ONEI contradicen los registros de destino antes de aplicar cualquier modelo (Figura <a href="#fig:mig" data-reference-type="ref" data-reference="fig:mig">1</a>). Para 2021 y 2022 la ONEI declara *llegadas* netas de $`+`$<!-- -->169 y $`+`$<!-- -->991, mientras que solo Estados Unidos registró 54 818 y 313 506 llegadas de cubanos en esos años. Una revisión sistemática de la serie publicada (`scripts/consistency_model.py`) devuelve 18 pruebas, de las cuales 7 fallan con severidad alta: dos de ellas (T2, los tres totales oficiales en conflicto para 2022 —129 049, 120 098 y 120 108, una dispersión del 7.5%; los totales de 2023 difieren en solo diez defunciones y no son materiales— y T4, la contradicción de 2023 entre tasa y denominador) usan únicamente fuentes oficiales, de modo que esas inconsistencias son internas a la serie publicada por la ONEI. La serie de 2023 muestra una caída poblacional de 1 033 543 personas en un solo año frente a un decrecimiento natural de 27 347, lo que implica un componente migratorio de 1 006 196: más del doble de cualquier salida anual documentada, y que se lee mejor como una corrección de rezago contabilizada como flujo de un año. La tasa bruta de mortalidad publicada para 2023 (11.5 por mil) implica una población media de 10.24 millones frente a los 10.57 millones de la serie publicada, una brecha de 334 000 personas; ambas cifras no pueden ser correctas a la vez.

La estandarización por causas solo es posible para 2021–2022, usando la propia submisión CIE-10 de Cuba a la OMS sobre denominadores de la ONEI 3.3, y la reportamos porque restringe la lectura anterior más de lo que la respalda. Las tasas brutas cubanas por causa son unas 1.9 veces sus valores estandarizados por edad, de modo que comparar tasas brutas cubanas con tasas regionales estandarizadas —habitual en el comentario público— sobrestima la posición de Cuba en torno al doble. Las tasas estandarizadas propias de Cuba para 2022 son 87.2 por 100 000 en cardiopatía isquémica y 50.4 en enfermedad cerebrovascular. Deliberadamente *no* formamos una razón frente a comparadores regionales: las cifras que suelen citarse (del orden de 105 y 34) no son reproducibles a partir de ninguna fuente que tengamos, y los ficheros brutos de la OMS no contienen ningún país latinoamericano con defunciones y población posteriores a 2020, de modo que la comparación no puede hacerse hoy en términos equiparables en ninguna dirección. Entre 2021 y 2022 *todas* las causas estandarizadas cayeron —todas las causas un 28%, respiratorias un 57%, circulatorias un 24%, cardiopatía isquémica un 26%, cerebrovasculares un 14%, diabetes un 36% y neoplasias un 6%— porque 2021 es un pico pandémico, que es el problema de línea base que hace que una ventana de dos años no informe sobre el deterioro de 2024–2025. Por eso no extraemos ninguna inferencia de los movimientos por causa en ninguna dirección. Un diagnóstico sí sobrevive, con un límite de alcance que importa: las causas mal definidas (R00–R99) se mantienen en 0.85–0.98% entre 2021 y 2023, lo que es evidencia contra un deterioro de la certificación *en esos años*. No existen datos por causa para 2024–2025, donde se concentra el exceso, de modo que la deriva de codificación en justamente los años que gobiernan el titular queda sin comprobar. El trabajo por causas no puede extenderse más allá de 2022 porque los denominadores de la ONEI 3.3 se detienen ahí, razón por la cual ninguna causa entra en la estimación de exceso.

Alrededor del **77%** de los emigrantes tienen entre 15 y 59 años y la edad mediana de quien se va es de unos 30 años (Figura <a href="#fig:mig" data-reference-type="ref" data-reference="fig:mig">1</a>); ambas son distribuciones a priori expertas sintetizadas de los informes de Albizu-Campos y no mediciones, igual que la proporción del 8% de mayores que gobierna la emigración de ancianos en la proyección. Entre quienes permanecen, la proporción oficial reportada de 60 años y más es de alrededor del 26.7% (edad mediana $`\sim`$<!-- -->45); nótese que el cuadro 3.12 de la ONEI proyecta 25.0% para 2025, y que 26.7% es una cifra reportada que no podemos reproducir a partir de los cuadros publicados. Ninguna de las dos es consistente con el escenario central. La salida vacía el centro de la pirámide y se lleva a quienes habrían tenido hijos (Coleman 2006; Lee and Mason 2014). El flujo es mayoritariamente femenino (Albizu-Campos Espiñeira 2023) y se concentra en edades laborales (Figura <a href="#fig:mig" data-reference-type="ref" data-reference="fig:mig">1</a>). La intensidad de la salida varía entre provincias: la emigración neta de La Habana reportada por la ONEI es de alrededor de **$`-`$<!-- -->33 por 1 000** en 2025 (el orden relativo de las provincias es más fiable que los niveles si la contabilidad migratoria nacional está sesgada; mapa en el suplemento (en inglés)). La selectividad de la salida y el envejecimiento que produce son dos vistas del mismo proceso (Figura <a href="#fig:mig" data-reference-type="ref" data-reference="fig:mig">1</a>).

<figure id="fig:mig" data-latex-placement="!htbp">
<img src="f15_migracion_es.png" />
<figcaption>La afirmación migratoria, en tres paneles. Izquierda: composición por edades de los emigrantes frente a los residentes que permanecen; la salida es selectiva. Centro: saldo migratorio que declara la ONEI frente a los cubanos que otros países registraron llegando; la ONEI reporta <em>llegadas</em> netas en 2021 y 2022. Derecha: el puente desde un piso documentado de asentados hasta el motor migratorio del escenario central. Solo la primera barra tiene carácter de libro mayor. El vaciamiento de las edades laborales del panel izquierdo es lo que impulsa el término de envejecimiento de la Figura <a href="#fig:attrib" data-reference-type="ref" data-reference="fig:attrib">5</a>.</figcaption>
</figure>

## Exceso de mortalidad respecto de la tabla de 2019

Reducir la crisis solo a la emigración es incompleto: la emigración puede revertirse, pero los nacimientos que no ocurrieron y una población residual envejecida no. Una distinción útil es la de **pérdida realizada** (dominada por la salida) frente a **inercia futura** (donde el decrecimiento natural pesa cada vez más). En 2019 el saldo natural era todavía ligeramente positivo ($`+`$<!-- -->636); en 2025 las defunciones superaron a los nacimientos en **68 150** (68 064 nacimientos frente a 136 214 defunciones; Figura <a href="#fig:scissors" data-reference-type="ref" data-reference="fig:scissors">2</a>). Ese déficit de 2025 iguala el pico de COVID de 2021 sin pandemia: el decrecimiento natural es ya estructural. La tasa global de fecundidad cayó a 1.29 hijos por mujer en 2025, la más baja desde 1958 y muy por debajo del reemplazo (2.1) (Díaz-Briquets 2014; Bongaarts and Sobotka 2012; Lesthaeghe 2010). La emigración se lleva mujeres jóvenes (flujo mayoritariamente femenino) y quienes permanecen posponen nacimientos ante la escasez. Los nacimientos cayeron un 38% (de $`\sim`$<!-- -->110 000 en 2019 a 68 000 en 2025). Un cálculo aproximado que reparta la caída en “mitad menos mujeres / mitad menor fecundidad” es *solo ilustrativo*: los denominadores de la fecundidad de la ONEI pueden estar ellos mismos inflados por mujeres ausentes, lo que sobrestimaría la mitad atribuida a la tasa; aquí no se afirma una descomposición formal de exposición y tasas específicas de fecundidad por edad. La proporción reportada de 60 y más pasa del 20.4% (2019) al 26.7% (2025) —cifra que, como se señaló arriba, no es reproducible a partir de los cuadros publicados, frente a la proyección del 25.0% del propio cuadro 3.12 de la ONEI— y hacia el 33% en 2035, bajo un stock vivo mayor que el del escenario central (ONEI 2025; Lee and Mason 2014). Bajo un stock menor y vaciado de jóvenes la proporción de ancianos sería mayor; cualquier cifra de $`\sim`$<!-- -->29% o $`\sim`$<!-- -->40% en gráficos acompañantes es un **bosquejo ilustrativo**, no una estimación por componentes de cohorte. La edad mediana alcanzó los **45** años en 2025 según el reporte oficial (Figura <a href="#fig:aging" data-reference-type="ref" data-reference="fig:aging">3</a>).

<figure id="fig:internal" data-latex-placement="!htbp">
<figure id="fig:scissors">
<img src="f2_tijera_es.png" />
<figcaption>Nacimientos frente a defunciones (“la tijera”): las defunciones duplican a los nacimientos en 2025.</figcaption>
</figure>
<figure id="fig:aging">
<img src="f4_envejece_es.png" />
<figcaption>Envejecimiento acelerado a medida que se van los adultos en edad laboral (estructura oficial).</figcaption>
</figure>
<figcaption>Motor demográfico interno: decrecimiento natural y envejecimiento acelerado.</figcaption>
</figure>

La esperanza de vida al nacer oficial alcanzó su máximo en 2011–13 (78.5 años) y bajó a 77.7 en 2018–20; una estimación independiente de 2021 la sitúa cerca de 71 años (Albizu-Campos Espiñeira 2023; Brønnum-Hansen et al. 2023). Esa caída es grande frente a las pérdidas internacionales de la era COVID (Aburto et al. 2022; Msemburi et al. 2023); la esperanza de vida reexpresa la mortalidad en lugar de corroborar de forma independiente el escenario central (series en el suplemento (en inglés)). Las defunciones infantiles subieron de 461 (2018) a 715 (2022); la tasa alcanzó 9.9 por mil en 2025 ($`+`$<!-- -->98% desde 2019).

La descomposición de la mortalidad responde directamente a la pregunta envejecimiento frente a colapso (Figura <a href="#fig:attrib" data-reference-type="ref" data-reference="fig:attrib">5</a>). Cuba registró 136 214 defunciones en 2025 frente a 109 080 en 2019 —27 134 más, o unas 31 300 una vez añadidas las defunciones no registradas estimadas— mientras el stock del escenario central es unos 2 millones menor (la serie oficial cae 1.76 millones en el mismo tramo). Entretanto, la población de 60 años y más subió de 2.31 millones (2019, observado) a unos 2.60 millones proyectados en 2025. Tres términos dan cuenta de ese aumento (las medianas no son aditivas, de modo que suman 31 500 y no 31 300). Una población residente menor en $`\sim`$<!-- -->2 millones debería haber reducido las defunciones anuales en unas **19 400**; el envejecimiento añadió unas **22 400**; y el residual de exceso respecto de la tabla de 2019 es de unas **28 500** al año (rango de sensibilidad a los supuestos: 18 600–38 200), o $`\sim`$<!-- -->297 por cada 100 000 sobre la población oficial. Los dos términos al alza son de magnitud comparable ($`\sim`$<!-- -->44% y $`\sim`$<!-- -->56% de su propia suma, no del aumento observado); ninguno por sí solo explica el aumento, y juntos lo superan porque la población menguante tira en sentido contrario. El puente basado en tasas brutas reportado en versiones anteriores de este trabajo cargaba a la crisis todo el desplazamiento etario y sobrestimaba el componente de colapso: $`\sim`$<!-- -->77 000 para 2024–2025 combinados frente a **50 100** (32 600–67 500) aquí.

El perfil temporal separa dos episodios distintos. El exceso respecto de la tabla de 2019 fue de unas 5 400 en 2020, alcanzó $`\sim`$<!-- -->61 900 en la ola de COVID-19 de 2021, retrocedieron a $`\sim`$<!-- -->12 800 (2022) y $`\sim`$<!-- -->11 900 (2023), y luego casi se duplicaron hasta $`\sim`$<!-- -->21 600 (2024) y $`\sim`$<!-- -->28 500 (2025). El valle de 2022–2023 separa la ola pandémica del alza posterior, de modo que el aumento de 2024–2025 no es una continuación del pico de 2021; coincide con las crisis de apagones, combustible, medicamentos y arbovirosis, aunque el residual por sí solo no permite descartar la mortalidad pos-aguda por COVID-19 ni cambios de codificación como contribuyentes. Excluyendo 2021 por completo, el total de exceso de 2022–2025 es de $`\sim`$**74 900** (47 000–103 100); incluyéndolo, 2020–2025 da $`\sim`$<!-- -->142 100 (105 400–180 500). Una continuación de escenario para 2026 llega a $`\sim`$<!-- -->32 300 (20 000–44 200), pero esa cifra hereda la continuación supuesta de $`+`$<!-- -->4% en defunciones y no es una observación. La mayor incertidumbre individual no está dentro de la simulación sino en la elección del contrafactual, y no está en el rango anterior. Mantener plana la mortalidad de 2019 es un supuesto, y ajustamos la tendencia precrisis en lugar de afirmarla. El resultado es que **la tendencia no es identificable**: la serie dispersa 2006–2019 (cuatro años son inutilizables, véanse las Advertencias) da $`+0.236\%`$/año ($`p=0.066`$, IC 95% $`-0.02`$ a $`+0.49`$) y la ventana contigua 2013–2019 da $`+0.678\%`$/año ($`p=0.064`$, IC $`-0.06`$ a $`+1.41`$). Ambos intervalos contienen el cero. Por eso *no* ajustamos la tendencia ni la propagamos, lo que fabricaría una precisión que la serie no sostiene; el ancla plana es una convención declarada, no un hallazgo. La sensibilidad siguiente usa en consecuencia los límites que los datos permiten y no las estimaciones puntuales: el límite superior de la ventana más inclinada ($`+1.41\%`$/año) da 18 500 para 2025, y la mejora del 0.5–1.5%/año de los pares regionales da 31 600–38 000. El rango completo, **18 500–38 000**, es de amplitud *comparable* al rango de sensibilidad que lo acompaña (19 600 frente a 19 600) y casi coincidente con él —pero ambos son ortogonales y miden cosas distintas, de modo que esa casi identidad es una coincidencia que el lector no debe tomar por acuerdo. El rango contrafactual no se propaga al rango reportado. El mismo ejercicio sobre la ventana acumulada mueve 2022–2025 de 74 200 a **45 200–103 300**, de modo que los 74 900 del resumen dependen del ancla plana del mismo modo. Como ambos son ortogonales, ninguno por separado es el total: combinarlos sitúa 2025 más cerca de 15 000–45 000, y no reportamos un intervalo único porque no existe una distribución a priori defendible sobre las elecciones contrafactuales con la que combinarlos. La dirección es genuinamente ambigua: las tendencias ajustadas de la propia Cuba sitúan el exceso por debajo del ancla plana (26 700 y 23 700), mientras que la mejora lograda por sus pares regionales lo situaría muy por encima (31 600–38 000). No afirmamos una dirección. Pasando al ruido interno del ancla y no a su elección: las tasas por edad promedio de 2017–2019 quedan a menos del 1.1% de las de 2019 a los 65 años y más, donde ocurre la mayoría de las defunciones, y ligeramente *por encima*, de modo que 2019 fue un año comparativamente bueno y el ancla no favorece el resultado; la diferencia queda holgadamente dentro del ruido del 2% de la tabla de tasas.

<figure id="fig:attrib" data-latex-placement="!htbp">
<img src="f14_atribuible_es.png" />
<figcaption>Por qué suben las defunciones mientras cae la población. Izquierda: cambio en las defunciones anuales frente a 2019, descompuesto en tamaño poblacional, envejecimiento y deterioro de tasas; el punto es el cambio neto observado incluidas las defunciones no registradas estimadas. Derecha: defunciones de exceso respecto de la tabla de 2019, mediana y rango de sensibilidad a los supuestos. 2026 es una continuación de escenario, no una observación. Las bandas son predictivas a priori bajo las marginales indicadas y comparten <span class="math inline"><em>D</em><sub>fac</sub></span> con el escenario central.</figcaption>
</figure>

## Población proyectada

Las fuentes que no depuran emigrantes (padrón electoral, denominador de salud del MINSAP) quedan altas y funcionan como techos blandos. Las construcciones que corrigen por salida (ocupación de viviendas $`\sim`$<!-- -->8.7 M; Albizu-Campos 8.0–8.6 M) quedan cerca del escenario central pero comparten con este estudio los supuestos de crítica migratoria; no son censos independientes. El oficial de 9.43 M queda entre ambas familias (Figura <a href="#fig:tri" data-reference-type="ref" data-reference="fig:tri">6</a>). La participación electoral cayó abruptamente entre 2018 y 2023; ese patrón es compatible con ausencia física pero también con abstención, logística y factores políticos, y *no* se usa como recuento de personas.

<figure id="fig:tri" data-latex-placement="!htbp">
<img src="f7_triangulacion_es.png" style="width:95.0%" />
<figcaption>Triangulación de los niveles de población a fin de 2025. El escenario central es el estimando del estudio (no un validador); Albizu y viviendas son anclas blandas y cargadas de supuestos.</figcaption>
</figure>

El Cuadro <a href="#tab:models" data-reference-type="ref" data-reference="tab:models">4</a> resume los tres escenarios. El enunciado primario de incertidumbre es la envolvente entre escenarios: frente al stock oficial de fin de 2021 (11.11 millones), la brecha a fin de 2025 abarca **1.97–2.79 millones**, o **17.8–25.1%**. El escenario central sitúa la población viva en **8.58 millones** (brecha **2.53 millones**, **22.8%**) frente a 9.43 millones oficiales, con el piso en 9.14 millones y el caso superior en 8.32 millones. La emigración explica alrededor del **92%** de la brecha central una vez contado el rezago previo a 2021 junto al flujo de 2022–2025; dentro del flujo solo, $`\sim`$<!-- -->91%. La continuación a fin de 2026 sitúa el escenario central cerca de **8.29 millones** (envolvente 8.02–8.84 millones). Al haber ahora una sola base, el titular tiene una sola forma: entre aproximadamente una de cada seis y una de cada cuatro personas contadas oficialmente en 2021 no está.

<div id="tab:models">

| Escenario | Brecha (M) | Brecha % | Pob. fin-2025 (M) | Pob. fin-2026 (M) |
|:---|---:|---:|---:|---:|
| *Nulo: ONEI al pie de la letra* | *1.68* | *15.1* | *9.43* | *9.14* |
| Conservador | 1.97 | 17.8 | 9.14 | 8.84 |
| **Central ajustado por crisis** | **2.53** | **22.8** | **8.58** | **8.29** |
| Superior de estrés | 2.79 | 25.1 | 8.32 | 8.02 |
| *Envolvente (excl. nulo)* | *1.97–2.79* | *17.8–25.1* | *8.32–9.14* | *8.02–8.84* |

Tres escenarios sobre una sola base: el stock oficial de fin de 2021 (11 113 215). Las estimaciones puntuales son de forma cerrada; las bandas del 90% dentro de cada escenario son dispersiones predictivas a priori No son intervalos de confianza, no tienen propiedad de cobertura, y ningún parámetro de este trabajo se informa con una verosimilitud. Versiones anteriores llevaban cinco conjuntos de priores; una variante ajustada por crisis (a 0.02 M del central) y un acompañante de reconstrucción vital se han retirado.

</div>

<figure id="fig:headline" data-latex-placement="!htbp">
<figure id="fig:pop">
<img src="f1_poblacion_es.png" />
<figcaption>Población oficial frente a población viva por escenario, 2021–2030 (trayectoria ilustrativa del escenario central en rojo; el tramo posterior a 2026 es un escenario de tendencia no probabilístico).</figcaption>
</figure>
<figure id="fig:cascade">
<img src="f3_cascada_es.png" />
<figcaption>Descomposición contable con medianas del escenario central (2021–2025); escenario ilustrativo, no una atribución identificada.</figcaption>
</figure>
<figcaption>Trayectoria poblacional principal y descomposición contable.</figcaption>
</figure>

En el plano regional, América Latina y el Caribe todavía crecen ($`\sim`$+$`0.7\%`$ anual; Cuadro <a href="#tab:region" data-reference-type="ref" data-reference="tab:region">6</a>, aproximaciones de WPP de la ONU y CEPAL). Cuba muestra una pérdida neta de población de alrededor de $`-`$<!-- -->3.3% anual en comparaciones sobre la trayectoria oficial reciente. Entre las contracciones en tiempos de paz impulsadas por la emigración, Venezuela es el par regional más cercano (Cuadro <a href="#tab:hist" data-reference-type="ref" data-reference="tab:hist">5</a>); los casos impulsados por desastres no se tratan como pares. Hacia **fin de 2026**, la continuación central implica una pérdida adicional de unas 300 000 personas: población viva cerca de **8.29 millones** (banda entre escenarios 8.02–8.84 M). Hacia fin de 2026 el escenario superior alcanza una brecha de $`\sim`$<!-- -->3.1 millones y el central $`\sim`$<!-- -->2.8 millones ($`\sim`$<!-- -->25%). Las trayectorias de tendencia ilustrativas hacia $`\sim`$<!-- -->7 millones en 2030 (Figura <a href="#fig:pop" data-reference-type="ref" data-reference="fig:pop">7</a>, tramo posterior a 2026) son solo escenarios.

<div id="tab:hist">

| Caso | Pérdida acum. | Anual aprox. | Motor dominante |
|:---|---:|---:|---:|
| Venezuela 2013–24 | $`\sim`$<!-- -->25% | 1–3% | emigración |
| Puerto Rico post-2017 (era María) | salida neta grande | — | emigración + desastre |
| Cuba 2021–25 (central) | $`\sim`$<!-- -->22.8% (base oficial) | $`\sim`$<!-- -->3–5% | emigración + interno |

Cuba frente a contracciones seleccionadas impulsadas por la emigración en tiempos de paz. La fila de Cuba usa el escenario central sobre la base oficial de 2021 y por tanto incluye una corrección de padrón previa a 2021 ($`U_0`$) más la puesta al día del rezago de la ONEI en 2023; es una discrepancia de stock, no un flujo 2021–25, y no es equiparable con los comparadores, que son pérdidas de población. Los comparadores son aproximados y no están armonizados por ventana temporal. La fila de Puerto Rico está confundida por el desastre del huracán María.

</div>

<div id="tab:region">

| País / región | Crecimiento anual |
|:---|---:|
| Guatemala | $`+1.7\%`$ |
| Bolivia | $`+1.4\%`$ |
| República Dominicana | $`+1.0\%`$ |
| México | $`+0.8\%`$ |
| Colombia | $`+0.7\%`$ |
| *América Latina y el Caribe* | $`+0.7\%`$ |
| Brasil | $`+0.4\%`$ |
| Chile | $`+0.3\%`$ |
| Uruguay | $`+0.1\%`$ |
| Venezuela | $`\approx 0\%`$ (tras $`\sim`$<!-- -->25% de pérdida 2013–24) |
| Cuba | $`-3.3\%`$ |

Crecimiento poblacional anual: Cuba frente a la región (aproximado; revisión 2024 de WPP de la ONU y CEPAL, redondeado).

</div>

# Discusión

## Migración

El único caso documentado de revisión a la baja del registro de defunciones es ilustrativo. Usamos la cifra publicada, pero el total previo a la revisión elevaría la mortalidad en exceso de 2022 de $`\sim`$<!-- -->12 700 a $`\sim`$<!-- -->21 900, y el total pospandémico 2022–2025 de $`\sim`$<!-- -->74 900 a $`\sim`$<!-- -->84 100. Este es el anclaje empírico de cuánta holgura tiene demostrablemente el registro: un 7.5% en un solo año, apenas por debajo del tope del 9% sobre $`D_{\mathrm{fac}}`$, razón por la cual ese tope se mantiene en lugar de elevarse. Acota la pregunta desde la observación y no desde una creencia previa, y corta en ambas direcciones: un registro que puede perder 8 951 defunciones sin explicación no es plenamente confiable, pero uno que publicó un alza del 54% en un solo año en 2021 (de 109 080 a 167 645) tampoco es uno que oculte a gran escala.

El saldo migratorio declarado por la ONEI para 2022 ($`+`$<!-- -->991) es incompatible con cientos de miles de llegadas de cubanos a Estados Unidos ese mismo año bajo cualquier conversión plausible de encuentros a emigrantes (los encuentros no son emigrantes netos únicos en proporción 1:1). Buena parte del éxodo se contabiliza en una sola revisión de 2023, compatible con una puesta al día rezagada del registro asentada en un único año. Incluso tras esa revisión, los saldos netos de 2024–2025 quedan solo ligeramente por encima de las entradas registradas únicamente en Estados Unidos, mientras que el saldo de 2025 admite 317 320 emigraciones externas brutas (neto $`-`$<!-- -->245 264): un déficit frente al piso multidestino, aunque el saldo de 2025 es internamente consistente. Por eso este trabajo trata el recuento oficial como un techo y lo contrasta con fuentes que corrigen por salida (Figura <a href="#fig:tri" data-reference-type="ref" data-reference="fig:tri">6</a>).

En conjunto: frente al stock oficial de fin de 2021, la brecha a fin de 2025 se sitúa entre 1.97 y 2.79 millones, o 17.8–25.1% (el enunciado primario). Bajo el escenario central, la población viva está cerca de 8.58 millones a fin de 2025 y no en los 9.43 millones oficiales: una brecha de 2.53 millones (22.8%), de la cual alrededor del 92% es emigración; el piso anclado en la ONEI queda en 9.14 millones. Hacia fin de 2026 la continuación central está cerca de 8.29 millones, llevando la brecha a aproximadamente una de cada cuatro personas. Junto a ese recuento —de cuya brecha de 2.53 millones, 1.68 millones son caída ya publicada por la ONEI y 0.85 millones la corrección de este trabajo— el exceso respecto de la tabla de 2019 corre a $`\sim`$<!-- -->28 500 defunciones al año a niveles de 2025 y a $`\sim`$<!-- -->74 900 acumuladas en 2022–2025, un costo mayor que lo que explica el envejecimiento por sí solo y alrededor de un tercio inferior a lo que implicaba para 2024–2025 el puente basado en tasas brutas. Un censo en 2026 realizado con prácticas estándar sería informativo; la banda de escenario de trabajo a fin de 2026 es de 8.02–8.84 millones y no la trayectoria de 10.9 millones de *World Population Prospects* bajo supuestos de emigración neta todavía bajos (United Nations, Department of Economic and Social Affairs, Population Division 2024).

## Exceso de mortalidad respecto de la tabla de 2019

Los dos motores se encuentran en la descomposición de la mortalidad, y leerla correctamente importa. La emigración se lleva adultos en edad laboral, lo que eleva la proporción de ancianos, lo que a su vez eleva las defunciones incluso con un sistema de salud inalterado: eso es lo que mide el término de envejecimiento: unas 22 400 defunciones adicionales al año. Cuánto de ese envejecimiento es inducido por la migración *no* se identifica aquí: el término se calcula sobre la estructura por edades observada de la ONEI, y la transición de la fecundidad cubana ya generaba envejecimiento décadas antes de la crisis, de modo que debe leerse como envejecimiento por todas las causas combinadas, de las cuales la salida selectiva es una. Encima de él se sitúa un deterioro de tasas de $`\sim`$<!-- -->28 500 defunciones al año que el envejecimiento no explica, concentrado en 2024–2025 y todavía en ascenso en el escenario de 2026. La asimetría relevante para la política pública es que la emigración puede revertirse, mientras que ni esas muertes ni los nacimientos que no ocurrieron pueden hacerlo. Dos propiedades hacen que la estimación de exceso sea más robusta que los escenarios poblacionales junto a los que se presenta: no depende de resolver la disputa migratoria, porque el número de ancianos se mantiene aproximadamente fijo y $`E_t`$ apenas se mueve entre la población oficial y la del escenario central; y es insensible al *nivel* del ancla, que la sensibilidad 2017–2019 deja esencialmente inalterado a los 60 años y más (*no* es insensible a su tendencia, que es la incertidumbre dominante señalada arriba). Sigue siendo condicional a que el registro de defunciones sea casi completo: un supuesto que el centinela de mortalidad infantil hace plausible para las muertes institucionales pero no demuestra, y que la distribución a priori de $`D_{\mathrm{fac}}`$ pretende absorber más que resolver. Su debilidad principal es la opuesta a la de los modelos poblacionales: el mecanismo no está identificado. Los apagones, los fallos de ambulancias y de diálisis por falta de combustible, la escasez de medicamentos, la oncología demorada y las olas de arbovirosis de 2025–2026 son todas vías plausibles, y ninguna se estima aquí por separado; la estimación es una asociación con el período de crisis, no una atribución por causa de muerte. Los indicadores de inseguridad alimentaria y anemia del PMA, y la caída del PIB agrícola, se discuten solo como vías *contextuales* amplificadoras (World Food Programme 2024); no entran en $`D_{\mathrm{fac}}`$ ni en la descomposición (Karlinsky and Kobak 2021; Msemburi et al. 2023).

## Población proyectada

El escenario central se mantiene porque la comprobación de consistencia con la mortalidad infantil reduce la necesidad de multiplicadores grandes de defunciones ocultas y concentra la incertidumbre residual en la migración (García et al. 2019; Pérez-Riverol 2026b). No es una estimación puntual identificada: la pérdida absoluta sigue siendo $`\sim`$<!-- -->91% migratoria bajo las distribuciones a priori del escenario central, y $`U_0`$ junto con $`M>1`$ pueden compartir un mismo defecto de padrón desactualizado. Los intervalos dentro de un escenario parecen falsamente precisos frente a la envolvente entre escenarios: la envolvente debe encabezar la lectura. El enunciado científico principal son los 0.85 millones en que el escenario central queda por debajo de la propia cifra de la ONEI para fin de 2025. La brecha de 2.53 millones (22.8%) frente a la base oficial de 2021 es la suma de esa corrección y los 1.68 millones que la ONEI ya ha publicado; ambas no deben citarse indistintamente. La salida es selectiva por edad y sexo; envejece la isla y deprime estructuralmente la fecundidad (Coleman 2006; Díaz-Briquets 2014; Lee and Mason 2014). El saldo natural, positivo en 2019, cayó a $`-`$<!-- -->68 150 en 2025.

# Advertencias y limitaciones

**Limitaciones.** No hay censo desde 2012; la regla de $`\sim`$<!-- -->24 meses de la ONEI para contabilizar emigrantes rezaga las salidas recientes; los microdatos de destino son incompletos; los totales administrativos de “asentados” en Estados Unidos no son el stock de la ACS; los supuestos de ocupación de viviendas son frágiles; los bosquejos de envejecimiento no son proyecciones por componentes de cohorte; la esperanza de vida reexpresa la mortalidad; las trayectorias 2026–2030 son escenarios. $`U_0`$ y $`M`$ pueden contar dos veces el rezago del padrón; los techos de encuentros en destino pueden inflar el número de personas únicas; los intervalos dentro de un escenario dan una falsa precisión frente a la incertidumbre estructural. La descomposición de la mortalidad usa cuatro grupos de edad porque es el conjunto más fino que comparten los cuadros 3.15 y 3.3 de la ONEI; ambos se detienen en 2022, de modo que la estructura por edades de 2023–2026 es una proyección por cohortes y no una observación, y la composición dentro del grupo de 65 y más después de 2022 entra como un parámetro residual de deriva. Su ancla de 2019 supone que no habría habido mejora contrafactual de la mortalidad cubana después de 2019, y comparte $`D_{\mathrm{fac}}`$ con el escenario central, por lo que no es independiente del escenario de recuento. El exceso respecto de la tabla de 2019 es una asociación con el período de crisis, no una atribución por causa de muerte. Los indicadores de inseguridad alimentaria son solo contextuales.

La serie precrisis estandarizada por edad no puede ajustarse sobre una ventana completa: los paneles de la ONEI 3.15 para 2009–2012 se leen como aproximadamente la mitad de las defunciones reales y un control de lectura los rechaza, de modo que la tendencia descansa en 10 años no contiguos (o 7 contiguos, que dan una tendencia casi tres veces mayor). En cualquiera de las dos ventanas la pendiente es estadísticamente indistinguible de cero, de modo que no hay tendencia precrisis que ajustar y el ancla plana debe leerse como una convención. La incertidumbre dominante en el estimando de mortalidad es la elección del contrafactual, no algo interno a la simulación, y se reporta por separado en lugar de integrarse en el rango.

**Estatus.** Este es un preprint y no ha sido revisado por pares. Los tres escenarios son narrativas a priori, no estimadores identificados de una población viva única, y las bandas reportadas son dispersiones predictivas a priori y no error muestral proveniente de los datos.

**Disponibilidad de datos y código.** Los cuadros de la ONEI y una hoja de afirmaciones legible por máquina están en el repositorio público <https://github.com/ypriverol/cubascience>, bajo `demographics/`. Acompañante interactivo: <https://ypriverol.github.io/cubascience/demographics/>. Los scripts Monte Carlo (`scripts/model_*.py`) y la descomposición de mortalidad (`scripts/attributable_mortality.py`) escriben resúmenes en `artifacts/`. PDF suplementario (solo en inglés): `manuscript/en/cuba-depopulation-2021-2026-supplement.pdf` (Pérez-Riverol 2026c). La literatura de terceros se cita, no se redistribuye.

**Conflictos de interés.** Ninguno declarado.

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-aburto2022" class="csl-entry">

Aburto, José Manuel, Jonas Schöley, Ilya Kashnitsky, et al. 2022. “Quantifying Impacts of the COVID-19 Pandemic Through Life-Expectancy Losses: A Population-Level Study of 29 Countries.” *International Journal of Epidemiology* 51 (1): 63–74. <https://doi.org/10.1093/ije/dyab207>.

</div>

<div id="ref-albizu2023" class="csl-entry">

Albizu-Campos Espiñeira, Juan Carlos. 2023. *Cuba: Çrisis Demográfica o Crisis Sistémica?* Horizonte Cubano. Cuba Capacity Building Project, Columbia Law School. <https://horizontecubano.law.columbia.edu/news/cuba-demographic-or-systemic-crisis>.

</div>

<div id="ref-albizu2024" class="csl-entry">

Albizu-Campos Espiñeira, Juan Carlos. 2024. *Cuba: Emigración, Vaciamiento Demográfico y Población, 2024*. Working paper / report.

</div>

<div id="ref-berdine2018" class="csl-entry">

Berdine, Gilbert, Vincent Geloso, and Benjamin Powell. 2018. “Cuban Infant Mortality and Longevity: Health Care or Repression?” *Health Policy and Planning* 33 (6): 755–57. <https://doi.org/10.1093/heapol/czy033>.

</div>

<div id="ref-bongaarts2009" class="csl-entry">

Bongaarts, John, and Tomáš Sobotka. 2012. “A Demographic Explanation for the Recent Rise in European Fertility.” *Population and Development Review* 38 (1): 83–120. <https://doi.org/10.1111/j.1728-4457.2012.00473.x>.

</div>

<div id="ref-bronnum2023" class="csl-entry">

Brønnum-Hansen, Henrik, Juan Carlos Albizu-Campos Espiñeira, Camila Perera, and Ingelise Andersen. 2023. “Trends in Mortality Patterns in Two Countries with Different Welfare Models: Comparisons Between Cuba and Denmark 1955–2020.” *Journal of Population Research* 40 (2). <https://doi.org/10.1007/s12546-023-09296-w>.

</div>

<div id="ref-coleman2006" class="csl-entry">

Coleman, David. 2006. “Immigration and Ethnic Change in Low-Fertility Countries: A Third Demographic Transition.” *Population and Development Review* 32 (3): 401–46. <https://doi.org/10.1111/j.1728-4457.2006.00131.x>.

</div>

<div id="ref-diazbriquets2014" class="csl-entry">

Díaz-Briquets, Sergio. 2014. “Accounting for Recent Fertility Swings in Cuba.” *Population and Development Review* 40 (4): 677–93. <https://doi.org/10.1111/j.1728-4457.2014.00006.x>.

</div>

<div id="ref-diazbriquets1982" class="csl-entry">

Díaz-Briquets, Sergio, and Lisandro Pérez. 1982. “Fertility Decline in Cuba: A Socioeconomic Interpretation.” *Population and Development Review* 8 (3): 513–38. <https://doi.org/10.2307/1972378>.

</div>

<div id="ref-eclac2022" class="csl-entry">

Economic Commission for Latin America and the Caribbean (ECLAC). 2022. *Demographic Observatory of Latin America and the Caribbean 2022: Population Trends in Latin America and the Caribbean*. United Nations.

</div>

<div id="ref-pagegarcia2020" class="csl-entry">

García, Jenny, Gerardo Correa, and Brenda Rousset. 2019. “Trends in Infant Mortality in Venezuela Between 1985 and 2016: A Systematic Analysis of Demographic Data.” *The Lancet Global Health* 7 (3): e331–36. <https://doi.org/10.1016/S2214-109X(18)30479-0>.

</div>

<div id="ref-hollerbach1984" class="csl-entry">

Hollerbach, Paula E., Sergio Díaz-Briquets, and Kenneth Hill. 1984. “Fertility Determinants in Cuba.” *International Family Planning Perspectives* 10 (1): 12–20. <https://doi.org/10.2307/2948029>.

</div>

<div id="ref-karlinsky2021" class="csl-entry">

Karlinsky, Ariel, and Dmitry Kobak. 2021. “Tracking Excess Mortality Across Countries During the COVID-19 Pandemic with the World Mortality Dataset.” *eLife* 10: e69336. <https://doi.org/10.7554/eLife.69336>.

</div>

<div id="ref-kishore2018" class="csl-entry">

Kishore, Nishant, Domingo Marqués, Ayesha Mahmud, et al. 2018. “Mortality in Puerto Rico After Hurricane Maria.” *New England Journal of Medicine* 379: 162–70. <https://doi.org/10.1056/NEJMsa1803972>.

</div>

<div id="ref-kitagawa1955" class="csl-entry">

Kitagawa, Evelyn M. 1955. “Components of a Difference Between Two Rates.” *Journal of the American Statistical Association* 50 (272): 1168–94. <https://doi.org/10.1080/01621459.1955.10501299>.

</div>

<div id="ref-lee2014" class="csl-entry">

Lee, Ronald, and Andrew Mason. 2014. “Is Low Fertility Really a Problem? Population Aging, Dependency, and Consumption.” *Science* 346 (6206): 229–34. <https://doi.org/10.1126/science.1250542>.

</div>

<div id="ref-lesthaeghe2010" class="csl-entry">

Lesthaeghe, Ron. 2010. “The Unfolding Story of the Second Demographic Transition.” *Population and Development Review* 36 (2): 211–51. <https://doi.org/10.1111/j.1728-4457.2010.00328.x>.

</div>

<div id="ref-pew_cuban" class="csl-entry">

Moslimani, Mohamad, and Jeffrey S. Passel. 2024. *Facts about the U.S. Cuban Immigrant Population*. Pew Research Center; <https://www.pewresearch.org/short-reads/>.

</div>

<div id="ref-msemburi2023" class="csl-entry">

Msemburi, William, Ariel Karlinsky, Victoria Knutson, Serge Aleshin-Guendel, Somnath Chatterji, and Jon Wakefield. 2023. “The WHO Estimates of Excess Mortality Associated with the COVID-19 Pandemic.” *Nature* 613: 130–37. <https://doi.org/10.1038/s41586-022-05522-2>.

</div>

<div id="ref-onei_census" class="csl-entry">

ONEI. 2022. *Census Postponement and Demographic Programme Notes*.

</div>

<div id="ref-onei_revision" class="csl-entry">

ONEI. 2024. *Effective Population Revision Reported to the National Assembly*.

</div>

<div id="ref-onei_2025" class="csl-entry">

ONEI. 2025. *Indicadores Demográficos 2025 and Anuario Demográfico Tables*. <a href="https://www.onei.gob.cu/poblacion-0" class="uri">Https://www.onei.gob.cu/poblacion-0</a>.

</div>

<div id="ref-repo" class="csl-entry">

Pérez-Riverol, Yasset. 2026a. *CubaScience Demographics Companion Repository*. <a href="https://github.com/ypriverol/cubascience" class="uri">Https://github.com/ypriverol/cubascience</a>.

</div>

<div id="ref-modeld" class="csl-entry">

Pérez-Riverol, Yasset. 2026b. *Model d Sentinel-Anchored Monte Carlo Implementation*. File `demographics/scripts/model_from_2021.py` in.

</div>

<div id="ref-modele_supp" class="csl-entry">

Pérez-Riverol, Yasset. 2026c. *Model e Vital Reconstruction (HSDS) — Supplementary Materials*. File `demographics/manuscript/en/cuba-depopulation-2021-2026-supplement.pdf` in.

</div>

<div id="ref-destinations" class="csl-entry">

Pérez-Riverol, Yasset. 2026d. *Settled Destinations Ledger (Aggregated Public Statistics)*. File `demographics/data/destinations_settled.csv` in.

</div>

<div id="ref-preston2001" class="csl-entry">

Preston, Samuel H., Patrick Heuveline, and Michel Guillot. 2001. *Demography: Measuring and Modeling Population Processes*. Blackwell.

</div>

<div id="ref-un_wpp" class="csl-entry">

United Nations, Department of Economic and Social Affairs, Population Division. 2024. *World Population Prospects 2024*. <a href="https://population.un.org/wpp/" class="uri">Https://population.un.org/wpp/</a>.

</div>

<div id="ref-cbp_encounters" class="csl-entry">

U.S. Customs and Border Protection. 2024. *Nationwide Encounters: Cuba*. <a href="https://www.cbp.gov/newsroom/stats/nationwide-encounters" class="uri">Https://www.cbp.gov/newsroom/stats/nationwide-encounters</a>.

</div>

<div id="ref-wfp_cuba" class="csl-entry">

World Food Programme. 2024. *Cuba Country Brief / Food-Security Assessments*.

</div>

</div>
