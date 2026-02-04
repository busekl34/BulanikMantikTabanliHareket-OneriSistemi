from flask import Flask, render_template, request
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

# ==================================================
# BULANIK MANTIK SİSTEMİ
# ==================================================

# Antecedent & Consequent
bmi = ctrl.Antecedent(np.arange(18.5, 40.1, 0.1), 'bmi')
fastfood = ctrl.Antecedent(np.arange(0, 101, 1), 'fastfood')
aktivite = ctrl.Antecedent(np.arange(30, 241, 1), 'aktivite')
hareket = ctrl.Consequent(np.arange(10, 181, 1), 'hareket')

# Üyelik Fonksiyonları
bmi['normal'] = fuzz.trimf(bmi.universe, [18.5, 21.5, 24.9])
bmi['fazla']  = fuzz.trimf(bmi.universe, [23, 27, 30])
bmi['obez']   = fuzz.trimf(bmi.universe, [28, 33, 37])
bmi['morbid'] = fuzz.trapmf(bmi.universe, [35, 38, 40, 40])

fastfood['dusuk']  = fuzz.trimf(fastfood.universe, [0, 20, 40])
fastfood['orta']   = fuzz.trimf(fastfood.universe, [30, 50, 70])
fastfood['yuksek'] = fuzz.trimf(fastfood.universe, [60, 80, 100])

aktivite['dusuk']  = fuzz.trapmf(aktivite.universe, [30, 30, 60, 100])
aktivite['orta']   = fuzz.trimf(aktivite.universe, [80, 130, 180])
aktivite['yuksek'] = fuzz.trimf(aktivite.universe, [160, 210, 240])

hareket['cok_az']    = fuzz.trimf(hareket.universe, [10, 20, 40])
hareket['az']        = fuzz.trimf(hareket.universe, [30, 50, 70])
hareket['orta']      = fuzz.trimf(hareket.universe, [60, 90, 120])
hareket['fazla']     = fuzz.trimf(hareket.universe, [100, 135, 170])
hareket['cok_fazla'] = fuzz.trapmf(hareket.universe, [150, 170, 180, 180])

# Kurallar (örnek: 36 kuralı buraya ekle)
rules = [

# NORMAL
ctrl.Rule(bmi['normal'] & fastfood['yuksek'] & aktivite['dusuk'],  hareket['fazla']),
ctrl.Rule(bmi['normal'] & fastfood['yuksek'] & aktivite['orta'],   hareket['orta']),
ctrl.Rule(bmi['normal'] & fastfood['yuksek'] & aktivite['yuksek'], hareket['az']),

ctrl.Rule(bmi['normal'] & fastfood['orta'] & aktivite['dusuk'],  hareket['orta']),
ctrl.Rule(bmi['normal'] & fastfood['orta'] & aktivite['orta'],   hareket['az']),
ctrl.Rule(bmi['normal'] & fastfood['orta'] & aktivite['yuksek'], hareket['cok_az']),

ctrl.Rule(bmi['normal'] & fastfood['dusuk'] & aktivite['dusuk'],  hareket['orta']),
ctrl.Rule(bmi['normal'] & fastfood['dusuk'] & aktivite['orta'],   hareket['az']),
ctrl.Rule(bmi['normal'] & fastfood['dusuk'] & aktivite['yuksek'], hareket['cok_az']),

# FAZLA
ctrl.Rule(bmi['fazla'] & fastfood['yuksek'] & aktivite['dusuk'],  hareket['cok_fazla']),
ctrl.Rule(bmi['fazla'] & fastfood['yuksek'] & aktivite['orta'],   hareket['fazla']),
ctrl.Rule(bmi['fazla'] & fastfood['yuksek'] & aktivite['yuksek'], hareket['orta']),

ctrl.Rule(bmi['fazla'] & fastfood['orta'] & aktivite['dusuk'],  hareket['fazla']),
ctrl.Rule(bmi['fazla'] & fastfood['orta'] & aktivite['orta'],   hareket['orta']),
ctrl.Rule(bmi['fazla'] & fastfood['orta'] & aktivite['yuksek'], hareket['az']),

ctrl.Rule(bmi['fazla'] & fastfood['dusuk'] & aktivite['dusuk'],  hareket['orta']),
ctrl.Rule(bmi['fazla'] & fastfood['dusuk'] & aktivite['orta'],   hareket['az']),
ctrl.Rule(bmi['fazla'] & fastfood['dusuk'] & aktivite['yuksek'], hareket['az']),

# OBEZ
ctrl.Rule(bmi['obez'] & fastfood['yuksek'] & aktivite['dusuk'],  hareket['cok_fazla']),
ctrl.Rule(bmi['obez'] & fastfood['yuksek'] & aktivite['orta'],   hareket['cok_fazla']),
ctrl.Rule(bmi['obez'] & fastfood['yuksek'] & aktivite['yuksek'], hareket['fazla']),

ctrl.Rule(bmi['obez'] & fastfood['orta'] & aktivite['dusuk'],  hareket['cok_fazla']),
ctrl.Rule(bmi['obez'] & fastfood['orta'] & aktivite['orta'],   hareket['fazla']),
ctrl.Rule(bmi['obez'] & fastfood['orta'] & aktivite['yuksek'], hareket['orta']),

ctrl.Rule(bmi['obez'] & fastfood['dusuk'] & aktivite['dusuk'],  hareket['fazla']),
ctrl.Rule(bmi['obez'] & fastfood['dusuk'] & aktivite['orta'],   hareket['orta']),
ctrl.Rule(bmi['obez'] & fastfood['dusuk'] & aktivite['yuksek'], hareket['az']),

# MORBID
ctrl.Rule(bmi['morbid'] & fastfood['yuksek'] & aktivite['dusuk'],  hareket['cok_fazla']),
ctrl.Rule(bmi['morbid'] & fastfood['yuksek'] & aktivite['orta'],   hareket['cok_fazla']),
ctrl.Rule(bmi['morbid'] & fastfood['yuksek'] & aktivite['yuksek'], hareket['cok_fazla']),

ctrl.Rule(bmi['morbid'] & fastfood['orta'] & aktivite['dusuk'],  hareket['cok_fazla']),
ctrl.Rule(bmi['morbid'] & fastfood['orta'] & aktivite['orta'],   hareket['cok_fazla']),
ctrl.Rule(bmi['morbid'] & fastfood['orta'] & aktivite['yuksek'], hareket['fazla']),

ctrl.Rule(bmi['morbid'] & fastfood['dusuk'] & aktivite['dusuk'],  hareket['cok_fazla']),
ctrl.Rule(bmi['morbid'] & fastfood['dusuk'] & aktivite['orta'],   hareket['fazla']),
ctrl.Rule(bmi['morbid'] & fastfood['dusuk'] & aktivite['yuksek'], hareket['orta']),
]

system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

# ==================================================
# ROUTES
# ==================================================
@app.route("/", methods=["GET", "POST"])
def index():
    sonuc = None
    bmi_value = None
    if request.method == "POST":
        try:
            boy = float(request.form["boy"])
            kilo = float(request.form["kilo"])
            fastfood_input = float(request.form["fastfood"])
            aktivite_input = float(request.form["aktivite"])
            
            boy_m = boy / 100
            bmi_value = kilo / (boy_m ** 2)
            
            sim.input['bmi'] = bmi_value
            sim.input['fastfood'] = fastfood_input
            sim.input['aktivite'] = aktivite_input
            sim.compute()
            
            sonuc = sim.output['hareket']
        except:
            sonuc = "Hata: Lütfen geçerli değerler girin."
    
    return render_template("index.html", sonuc=sonuc, bmi=bmi_value)

if __name__ == "__main__":
    app.run(debug=True)
