from fhirclient import client
import fhirclient.models.observation as o
import fhirclient.models.codeableconcept as cc
import fhirclient.models.coding as c
import fhirclient.models.fhirreference as fr
import fhirclient.models.fhirdate as fd
import json
import requests

def write(server_url, system, code, patient, value):
    observation = o.Observation()
    observation.status = "final"

    observation.subject = fr.FHIRReference()
    observation.subject.reference = ("Patient/%s" % patient)

    observation.code = cc.CodeableConcept()
    tmp = c.Coding()
    tmp.system = system
    tmp.code = code
    observation.code.coding = [tmp]

    observation.valueString = str(value)
    observation.effectiveDateTime = fd.FHIRDate("2017-11-28T00:00:00+00:00")

    #write json obj
    json_obj = observation.as_json()
    json_obj["resourceType"] = "Observation"
    print(json.dumps(json_obj))
    requests.post(server_url + "Observation", json=json_obj)