"""These functions access different rhyme apis, rhymebrain being the best because no api key is needed"""

import requests
import json


def get_rhymes_datamuse(word: str):
    datamuse_url = f"https://api.datamuse.com/words?sl={word}&rel_[hom]"
    rhymes = requests.get(datamuse_url)
    return rhymes.text


def get_rhymes_apinijas(word: str):
    apinijas_url = f"https://api.api-ninjas.com/v1/rhyme?word={word}"
    rhymes = requests.get(apinijas_url, headers={'X-Api-Key': 'TR8quurG3YxwbLc0Om25Ew==gvvAGRrm25T5awUA'})
    return rhymes.text


def get_rhymes_rhymebrain(word: str):
    rhymebrain_url = f"https://rhymebrain.com/talk?function=getRhymes&word={word}"
    try:
        rhymes = requests.get(rhymebrain_url)
        if rhymes.status_code == 200:
            return [dic['word'] for dic in json.loads(rhymes.text) if int(dic['score']) == 300]
        else:
            return ["", "An Error Occurred!", "Something went wrong with the site."]
    except:
        return ["", "An Error Occurred!", "Please check your internet connection."]


if __name__ == '__main__':
    print(get_rhymes_rhymebrain("Malone"))
