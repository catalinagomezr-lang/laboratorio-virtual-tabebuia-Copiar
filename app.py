import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq

st.set_page_config(page_title='Laboratorio virtual | Tabebuia rosea',page_icon='🧪',layout='wide')
st.markdown('''<style>.stApp{background:#f8fcf8}h1,h2,h3{color:#185b32}div[data-testid="stSidebar"]{background:#eaf5ec}.stButton button{background:#237b46;color:white}</style>''',unsafe_allow_html=True)
st.title('Laboratorio virtual · Universidad del Quindío')
st.caption('Programa de Química | Fracciones de Tabebuia rosea frente a Toxoplasma gondii')
st.info('Herramienta educativa. Los valores generados por los modelos son simulados y no constituyen resultados experimentales ni protocolos de manipulación del parásito.')
sections=['Presentación','Materiales y equipos','Fracciones y diluciones','Citotoxicidad · Alamar Blue','Actividad antiparasitaria','Análisis integrado','Equilibrio químico','Equilibrio de fases','Cinética de primer orden','Respuesta en función del tiempo','Electroquímica']
page=st.sidebar.radio('Secciones del laboratorio',sections)
st.sidebar.caption('Versión web interactiva basada en el cuaderno original de Google Colab.')
def plot(x,y,xlabel,ylabel,title):
 fig,ax=plt.subplots(figsize=(7,3.5));ax.plot(x,y,color='#21854b',lw=2.5);ax.set(xlabel=xlabel,ylabel=ylabel,title=title);ax.grid(alpha=.2);st.pyplot(fig);plt.close(fig)
def frac():return st.selectbox('Fracción', ['Fracción 1','Fracción 2','Fracción 3'])
if page=='Presentación':
 st.header('Contexto de la práctica')
 st.write('Evaluación educativa de tres fracciones de la corteza interna de **Tabebuia rosea** y su posible efecto sobre **Toxoplasma gondii**. Las fracciones fueron obtenidas en la Universidad Tecnológica de Pereira y suministradas al grupo GEPAMOL para su evaluación.')
 st.subheader('Objetivos')
 st.write('Explorar la citotoxicidad en células hospedadoras, la respuesta antiparasitaria aparente y la interpretación de curvas concentración–respuesta, vinculando los resultados con conceptos fisicoquímicos.')
 st.warning('La práctica del cuaderno trabaja con taquizoítos. No debe confundirse con el proyecto independiente sobre bradizoítos.')
elif page=='Materiales y equipos':
 st.header('Materiales y equipos')
 st.write('Elementos mencionados en el cuaderno: placas de 96 pozos, micropipetas, incubador, microscopio, lector de microplacas, material de vidrio y reactivos para ensayos colorimétricos y de fluorescencia.')
 st.write('Ensayo de citotoxicidad: Alamar Blue (resazurina/resorufina). Ensayo antiparasitario: lectura colorimétrica asociada a β-galactosidasa y X-Gal.')
 st.caption('Esta versión presenta la información en texto; la galería SVG original permanece en el cuaderno de Colab.')
elif page=='Fracciones y diluciones':
 st.header('Diluciones de las fracciones')
 f=frac();stock=st.number_input('Concentración de solución madre (mM)',.1,100.,20.,.1);target=st.slider('Concentración deseada (µM)',1,360,100);vol=st.number_input('Volumen final (µL)',100.,10000.,1000.,100.)
 v=target*vol/(stock*1000);pct=v/vol*100
 a,b=st.columns(2);a.metric('Volumen de solución madre',f'{v:.2f} µL');b.metric('DMSO final estimado',f'{pct:.2f} %')
 st.write('C₁V₁ = C₂V₂. El porcentaje de DMSO supone que la solución madre utiliza DMSO puro.')
 if pct>1:st.warning('La proporción calculada supera 1 % de DMSO. Revisar la compatibilidad con el control de vehículo antes de interpretar datos.')
elif page=='Citotoxicidad · Alamar Blue':
 st.header('Citotoxicidad · Alamar Blue')
 st.write('Modelo educativo de viabilidad relativa en células hospedadoras. Ensayo descrito en el cuaderno: HFF, lectura de fluorescencia con excitación 530/25 nm y emisión 590/25 nm.')
 f=frac();mode=st.radio('Tipo de datos',['Simulación','Ingreso de datos reales'],horizontal=True)
 if mode=='Simulación':
  ec=st.slider('Concentración media del efecto (µM)',1,360,100);maximum=st.slider('Reducción máxima de viabilidad (%)',0,100,80);c=st.slider('Concentración de interés (µM)',1,360,100)
  x=np.linspace(1,360,180);y=100-maximum*x/(ec+x);plot(x,y,'Concentración (µM)','Viabilidad relativa (%)','Curva simulada');st.metric('Viabilidad estimada',f'{100-maximum*c/(ec+c):.1f} %')
 else:
  control=st.number_input('Fluorescencia control',min_value=.001,value=1000.);sample=st.number_input('Fluorescencia muestra',min_value=0.,value=800.);blank=st.number_input('Blanco de fluorescencia',min_value=0.,value=0.)
  if control>blank:st.metric('Viabilidad relativa aparente',f'{100*(sample-blank)/(control-blank):.1f} %')
  else:st.error('El control debe superar el blanco.')
 st.caption('Una reducción de fluorescencia no demuestra por sí sola muerte celular: considerar blancos e interferencias.')
elif page=='Actividad antiparasitaria':
 st.header('Actividad antiparasitaria aparente')
 st.write('Análisis educativo de la señal del ensayo colorimétrico con β-galactosidasa. El cuaderno menciona lecturas a 420 y 615 nm; para datos reales debe aplicarse la corrección validada por el método.')
 f=frac();mode=st.radio('Datos',['Simulados','Lecturas reales'],horizontal=True)
 if mode=='Simulados':
  ic=st.slider('IC₅₀ hipotética (µM)',1,360,90);maxi=st.slider('Inhibición máxima (%)',1,100,95);x=np.linspace(1,360,180);y=maxi*x/(ic+x);plot(x,y,'Concentración (µM)','Inhibición aparente (%)','Curva simulada');st.caption('La IC₅₀ mostrada es un parámetro del modelo, no una medición.')
 else:
  ctrl=st.number_input('Absorbancia control corregida',min_value=.001,value=1.);sample=st.number_input('Absorbancia muestra corregida',min_value=0.,value=.6)
  st.metric('Inhibición aparente',f'{100*(1-sample/ctrl):.1f} %')
  st.warning('Antes de usar lecturas reales, definir y aplicar el tratamiento validado de las señales a 420 y 615 nm y los blancos.')
elif page=='Análisis integrado':
 st.header('Comparación de fracciones')
 mode=st.radio('Origen de los valores',['Ejemplo simulado','Ingreso manual'],horizontal=True)
 rows=[]
 for i in range(1,4):
  with st.expander(f'Fracción {i}',expanded=True):
   a,b=st.columns(2);v=a.slider('Viabilidad (%)',0.,100.,float([90,75,85][i-1]),key=f'v{i}');inh=b.slider('Inhibición (%)',0.,100.,float([40,65,80][i-1]),key=f'i{i}');rows.append({'Fracción':f'Fracción {i}','Viabilidad (%)':v,'Inhibición (%)':inh})
 st.dataframe(pd.DataFrame(rows),hide_index=True,use_container_width=True)
 st.write('Referencia didáctica: ≥80 % de viabilidad y ≥50 % de inhibición; **no** son criterios de validación experimental.')
 st.caption('No se calcula CC₅₀, IC₅₀ ni índice de selectividad con una sola concentración.')
elif page=='Equilibrio químico':
 st.header('Equilibrio químico: A + B ⇌ C + D')
 K=st.number_input('Constante Kc',min_value=.001,max_value=1000.,value=2.);a=st.slider('[A] inicial (M)',.1,5.,1.);b=st.slider('[B] inicial (M)',.1,5.,1.);c=st.slider('[C] inicial (M)',0.,5.,0.);d=st.slider('[D] inicial (M)',0.,5.,0.)
 Q=c*d/(a*b);low=-min(c,d)+1e-10;high=min(a,b)-1e-10
 def fun(z):return (c+z)*(d+z)-K*(a-z)*(b-z)
 z=brentq(fun,low,high);st.metric('Q inicial',f'{Q:.3f}');st.metric('Avance hacia productos (+) o reactivos (−)',f'{z:.4f} M');st.dataframe(pd.DataFrame({'Especie':['A','B','C','D'],'Equilibrio (M)':[a-z,b-z,c+z,d+z]}),hide_index=True)
 st.caption('Modelo hipotético, no representa una reacción identificada en las fracciones.')
elif page=='Equilibrio de fases':
 st.header('Distribución entre dos fases')
 mass=st.number_input('Masa total (mg)',.1,10000.,100.);va=st.number_input('Volumen acuoso (mL)',1.,1000.,100.);vo=st.number_input('Volumen orgánico (mL)',1.,1000.,100.);kd=st.number_input('Coeficiente de distribución KD = Corg/Caq',.001,1000.,.1)
 ma=mass*va/(va+kd*vo);mo=mass-ma
 st.dataframe(pd.DataFrame({'Fase':['Acuosa','Orgánica'],'Masa (mg)':[ma,mo],'Concentración (mg/mL)':[ma/va,mo/vo]}),hide_index=True)
 st.bar_chart(pd.DataFrame({'Masa (mg)':[ma,mo]},index=['Acuosa','Orgánica']))
 st.caption('Modelo de reparto ideal entre fases hipotéticas. No describe el proceso de extracción original de las fracciones.')
elif page=='Cinética de primer orden':
 st.header('Cinética de primer orden: A → B')
 a=st.slider('Concentración inicial [A]₀ (M)',.1,5.,1.);k=st.slider('Constante k (tiempo⁻¹)',.001,1.,.1);tmax=st.slider('Tiempo máximo (unidades arbitrarias)',1,100,48);t=np.linspace(0,tmax,200);y=a*np.exp(-k*t)
 plot(t,y,'Tiempo','[A] (M)','Decaimiento de primer orden');st.metric('Vida media',f'{np.log(2)/k:.2f} unidades de tiempo')
 st.caption('Reacción genérica didáctica; no identifica una vía de acción de las fracciones.')
elif page=='Respuesta en función del tiempo':
 st.header('Modelo de respuesta aparente en el tiempo')
 f=frac();C=st.slider('Concentración (µM)',1,360,100);ec=st.slider('EC₅₀ hipotética (µM)',1,360,90);imax=st.slider('Efecto máximo (%)',1,100,90);k=st.slider('Constante aparente de respuesta (h⁻¹)',.001,.5,.06);t=np.linspace(0,72,200);inh=imax*C/(ec+C)*(1-np.exp(-k*t))
 plot(t,inh,'Tiempo (h)','Inhibición aparente (%)','Respuesta temporal simulada');st.dataframe(pd.DataFrame({'Tiempo (h)':[6,12,24,48,72],'Inhibición simulada (%)':[round(imax*C/(ec+C)*(1-np.exp(-k*v)),2) for v in [6,12,24,48,72]]}),hide_index=True)
 st.caption('Modelo fenomenológico ilustrativo, no validado para la práctica.')
elif page=='Electroquímica':
 st.header('Ecuación de Nernst · celda hipotética')
 st.latex(r'M(s)+N^{2+}(aq)\rightarrow M^{2+}(aq)+N(s)')
 ea=st.slider('Potencial estándar de reducción M²⁺/M (V)',-2.,2.,-.76);ec=st.slider('Potencial estándar de reducción N²⁺/N (V)',-2.,2.,.34);ca=st.number_input('[M²⁺] (M)',.001,10.,1.);cc=st.number_input('[N²⁺] (M)',.001,10.,1.);temp=st.slider('Temperatura (°C)',0,100,25)
 e0=ec-ea;Q=ca/cc;E=e0-(8.314462618*(temp+273.15)/(2*96485.33212))*np.log(Q);dg=-2*96485.33212*E/1000
 st.metric('E° celda',f'{e0:.3f} V');st.metric('Potencial E',f'{E:.3f} V');st.metric('ΔG',f'{dg:.2f} kJ/mol');st.write('Sentido escrito:', 'espontáneo' if E>1e-9 else 'en equilibrio' if abs(E)<=1e-9 else 'no espontáneo')
 x=np.logspace(-3,1,120);y=e0-(8.314462618*(temp+273.15)/(2*96485.33212))*np.log(x/cc);plot(x,y,'[M²⁺] (M)','Potencial (V)','Nernst: variación con la concentración')
 st.caption('Celda ideal hipotética; no se atribuye esta reacción a Tabebuia rosea.')
st.divider();st.caption('Universidad del Quindío · Recurso didáctico interactivo. Verificar todos los cálculos y condiciones antes de uso académico formal.')
