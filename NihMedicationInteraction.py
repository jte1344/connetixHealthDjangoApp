import requests

# Base API URL of nih.gov
api_url_base = 'https://rxnav.nlm.nih.gov/REST'

# Extension to rxcui search api
api_rxcui = '/rxcui.json?'

# Extension to medication interaction api
api_interaction = '/interaction/list.json?'

# calls rxcui api to grab medication's rxcui id based on medication's name
# stores json outputs to rxcui_output and returns
def grab_rxcui(medication_name):
    medication_string = "name=" + medication_name + "&search=1"
    rxcui_response = requests.get(api_url_base + api_rxcui, medication_string)
    rxcui_ouput = rxcui_response.json()

#   print(json.dumps(rxcui_ouput, indent=4, sort_keys=True))                                                 DEBUG LINE
    return rxcui_ouput

# calls medication interaction api with given rxcui ids
# stores json output to interaction_output and returns
def grab_interactions(rxcuis):
    rxcui_param = "rxcuis=" + rxcuis + "&sources=DrugBank"
    interaction_response = requests.get(api_url_base + api_interaction, rxcui_param)
    interaction_output = interaction_response.json()

#   print(json.dumps(interaction_output, indent=4, sort_keys=True))                                          DEBUG LINE
    return interaction_output

def call_interactions(medication_list):
    medication_list = medication_list.replace(", ", ",")
    medication_list = medication_list.split(",")
    warning = []

    # calls grab_rxcui to get medications rxcui ids
    # places json outputs into rxcui_list
    rxcui_list = []
    for medication in medication_list:
        rxcui_list.append(grab_rxcui(medication))

    # appends all rxcuis into a string for grab_interactions parameter
    rxcui_string = ""
    for rxcui in rxcui_list:
        if "rxnormId" in rxcui['idGroup']:
#           print(rxcui['idGroup']['rxnormId'][0])                                                           DEBUG LINE
            if rxcui != rxcui_list[-1] and rxcui_list.__len__() > 1:
                rxcui_string = rxcui_string + rxcui['idGroup']['rxnormId'][0] + "+"
            else:
                rxcui_string = rxcui_string + rxcui['idGroup']['rxnormId'][0]
        else:
            warning.append("Invalid medication name entered...")

    # grabs drug interactions of given medications
    drug_interactions = grab_interactions(rxcui_string)

    # print resulting interactions between drugs to console
    interaction_list = []
    if rxcui_list.__len__() > 1:
        if "fullInteractionTypeGroup" in drug_interactions:
            warning.append("Potential interactions between the listed medications:")
            warning.append("*Information given based off active ingredient")
            for interaction in drug_interactions['fullInteractionTypeGroup'][0]['fullInteractionType']:
                interaction_list.append(interaction['interactionPair'][0]["description"])
        else:
            warning.append("No interactions found between the listed medications.")
    data = {"User Input:": medication_list, "Warning": warning, "Interactions": interaction_list}

    return data
