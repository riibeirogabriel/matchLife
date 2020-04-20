import requests
import json
from flask import Flask, render_template
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


'''if __name__ == "__main__":
    print(cpf_analize(11855727676))
    print(person_insurance_simulation(11321351000110, "YZ",
                                      "Luis Inacio gonzaga",
                                      11855727676,
                                      "1980-10-20T00:00:00", "2410-05",
                                      5000.0, 1, "MA"))'''


app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
