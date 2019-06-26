import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        # restful json
        # 三元表达式简化代码
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text

        # if r.status_code == 200:
        #     if return_json:
        #         return r.json()
        #     else:
        #         return r.text
        # else:
        #     if return_json:
        #         return {}

        #     else:
        #         return ''

