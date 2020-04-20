import requests
import json
from flask import Flask, render_template, request
api_serpro_cpf_url = "https://gateway.gr1d.io/sandbox/serpro/consulta-cpf/v1"\
                     "/cpf/"
api_mongeral_aegon_insurance = "https://gateway.gr1d.io/sandbox/mongeralaegon"\
                               "/v1/simulacao"


def cpf_analize(cpf_number):
    headers = {"X-Api-Key": "7daeffeb-c080-4ac3-8181-4a670d6abdb1"}
    response = requests.get(api_serpro_cpf_url + str(cpf_number),
                            headers=headers)

    json_object = json.loads(json.dumps(response.json()))
    return json.dumps(json_object, indent=2)


def person_insurance_simulation(cnpj, codigoModeloProposta, name, cpf,
                                birth_date, work, earn, gender, uf):
    params = (("cnpj", cnpj), ("codigoModeloProposta", codigoModeloProposta))
    headers = {"X-Api-Key": "1e0d86b2-d0b2-4ddb-96b4-cdc907f7e5a8"}
    body = {
            "simulacoes": [
                {
                    "proponente": {
                        "tipoRelacaoSeguradoId": 1,
                        "nome": name,
                        "cpf":  cpf,
                        "dataNascimento": birth_date,
                        "profissaoCbo": work,
                        "renda": earn,
                        "sexoId": gender,
                        "uf": uf,
                        "declaracaoIRId": 1
                    },
                    "periodicidadeCobrancaId": 30,
                    "prazoCerto": 30
                    }
            ]
            }

    response = requests.post(api_mongeral_aegon_insurance, params=params,
                             headers=headers, json=body)
    json_object = json.loads(json.dumps(response.json()))
    return json.dumps(json_object, indent=2)


app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/submit', methods=['POST', 'GET'])
def ensurance_simultaion():
    print(request.form['cpf'])
    return render_template(person_insurance_simulation(11321351000110,
                           request.form['codigoModeloProposta'],
                           request.form['name'],
                           request.form['cpf'],
                           "1980-10-20T00:00:00",
                           "2410-05",
                           request.form['earn'],
                           1,
                           request.form['uf']))

@app.route('/cpf', methods=['POST', 'GET'])
def cpf_validate():
    return render_template(     cpf_analize(request.form['cpf']))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
