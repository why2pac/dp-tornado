# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class JsonController(Controller):
    def get(self):
        obj = {
            't': 'hello',
            'n': 12356,
            'r': {
                't1': [1, 2, 3],
                't2': (1, 2, 3)
            }
        }

        obj_serialized_min = '{"n":12356,"r":{"t1":[1,2,3],"t2":[1,2,3]},"t":"hello"}'
        obj_serialized_beautify = """{
    "n": 12356,
    "r": {
        "t1": [
            1,
            2,
            3
        ],
        "t2": [
            1,
            2,
            3
        ]
    },
    "t": "hello"
}"""

        # self.helper.string.serialization

        text_serialized_min = self.helper.string.serialization.serialize(obj, method='json', beautify=False)
        text_serialized_beautify = self.helper.string.serialization.serialize(obj, method='json', beautify=True)

        assert(text_serialized_min == obj_serialized_min)
        assert(len(text_serialized_beautify.split('\n')) == len(obj_serialized_beautify.split('\n')))

        obj_deserialized_min = self.helper.string.serialization.deserialize(obj_serialized_min)
        obj_deserialized_beautify = self.helper.string.serialization.deserialize(obj_serialized_beautify)

        for k, v in obj.items():
            if isinstance(v, (dict, )):
                for kk, vv in v.items():
                    if isinstance(vv, (tuple, list)):
                        assert(list(vv) == list(obj_deserialized_min[k][kk]))
                        assert(list(vv) == list(obj_deserialized_beautify[k][kk]))

            else:
                assert(v == obj_deserialized_min[k])
                assert(v == obj_deserialized_beautify[k])

        # self.helper.string.serialization.json

        text_serialized_min = self.helper.string.serialization.json.stringify(obj, beautify=False)
        text_serialized_beautify = self.helper.string.serialization.json.stringify(obj, beautify=True)

        assert(text_serialized_min == obj_serialized_min)
        assert(len(text_serialized_beautify.split('\n')) == len(obj_serialized_beautify.split('\n')))

        obj_deserialized_min = self.helper.string.serialization.json.parse(obj_serialized_min)
        obj_deserialized_beautify = self.helper.string.serialization.json.parse(obj_serialized_beautify)

        for k, v in obj.items():
            if isinstance(v, (dict, )):
                for kk, vv in v.items():
                    if isinstance(vv, (tuple, list)):
                        assert(list(vv) == list(obj_deserialized_min[k][kk]))
                        assert(list(vv) == list(obj_deserialized_beautify[k][kk]))

            else:
                assert(v == obj_deserialized_min[k])
                assert(v == obj_deserialized_beautify[k])

        # self.helper.serialization

        text_serialized_min = self.helper.serialization.serialize(obj, method='json', beautify=False)
        text_serialized_beautify = self.helper.serialization.serialize(obj, method='json', beautify=True)

        assert(text_serialized_min == obj_serialized_min)
        assert(len(text_serialized_beautify.split('\n')) == len(obj_serialized_beautify.split('\n')))

        obj_deserialized_min = self.helper.serialization.deserialize(obj_serialized_min)
        obj_deserialized_beautify = self.helper.serialization.deserialize(obj_serialized_beautify)

        for k, v in obj.items():
            if isinstance(v, (dict, )):
                for kk, vv in v.items():
                    if isinstance(vv, (tuple, list)):
                        assert(list(vv) == list(obj_deserialized_min[k][kk]))
                        assert(list(vv) == list(obj_deserialized_beautify[k][kk]))

            else:
                assert(v == obj_deserialized_min[k])
                assert(v == obj_deserialized_beautify[k])

        # self.helper.string.serialization.json

        text_serialized_min = self.helper.serialization.json.stringify(obj, beautify=False)
        text_serialized_beautify = self.helper.serialization.json.stringify(obj, beautify=True)

        assert(text_serialized_min == obj_serialized_min)
        assert(len(text_serialized_beautify.split('\n')) == len(obj_serialized_beautify.split('\n')))

        obj_deserialized_min = self.helper.string.serialization.json.parse(obj_serialized_min)
        obj_deserialized_beautify = self.helper.string.serialization.json.parse(obj_serialized_beautify)

        for k, v in obj.items():
            if isinstance(v, (dict, )):
                for kk, vv in v.items():
                    if isinstance(vv, (tuple, list)):
                        assert(list(vv) == list(obj_deserialized_min[k][kk]))
                        assert(list(vv) == list(obj_deserialized_beautify[k][kk]))

            else:
                assert(v == obj_deserialized_min[k])
                assert(v == obj_deserialized_beautify[k])

        self.finish('done')
