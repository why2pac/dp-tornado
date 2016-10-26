# -*- coding: utf-8 -*-


import boto3

from dp_tornado.engine.helper import Helper as dpHelper


class ItemHelper(dpHelper):
    def put(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            items,
            overwrite_by_pkeys=None):
        items = items if self.helper.misc.type.check.array(items) else (items, )

        return self._batch(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            region_name=region_name,
            table_name=table_name,
            items=items,
            fn_key='Item',
            fn_proc='put_item',
            overwrite_by_pkeys=overwrite_by_pkeys)

    def remove(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            keys,
            overwrite_by_pkeys=None):
        keys = keys if self.helper.misc.type.check.array(keys) else (keys, )

        return self._batch(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            region_name=region_name,
            table_name=table_name,
            items=keys,
            fn_key='Key',
            fn_proc='delete_item',
            overwrite_by_pkeys=overwrite_by_pkeys)

    def get(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            keys):
        multi = True if self.helper.misc.type.check.array(keys) else False
        keys = keys if self.helper.misc.type.check.array(keys) else (keys, )
        output = []

        try:
            table = self.helper.web.aws.dynamodb.table.get(
                access_key_id=access_key_id,
                secret_access_key=secret_access_key,
                region_name=region_name,
                table_name=table_name)

            if not table:
                return False

            for key in keys:
                got = table.get_item(Key=key)

                if not got or 'Item' not in got:
                    continue

                output.append(got['Item'])

            return output if multi else (output[0] if output else [])

        except Exception as e:
            self.logging.exception(e)

            return False

    def query(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            count=False,
            **kwargs):
        table = self.helper.web.aws.dynamodb.table.get(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            region_name=region_name,
            table_name=table_name)

        if count:
            kwargs['Select'] = 'COUNT'

        try:
            result = table.query(**kwargs)
        except Exception as e:
            self.logging.exception(e)

            return False

        if count:
            if 'Count' not in result:
                return False

            return result['Count']

        if not result or 'Items' not in result:
            return []

        return result['Items']

    def scan(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            count=False,
            **kwargs):
        table = self.helper.web.aws.dynamodb.table.get(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            region_name=region_name,
            table_name=table_name)

        if count:
            kwargs['Select'] = 'COUNT'

        try:
            result = table.scan(**kwargs)
        except Exception as e:
            self.logging.exception(e)

            return False

        if count:
            if 'Count' not in result:
                return False

            return result['Count']

        if not result or 'Items' not in result:
            return []

        return result['Items']

    def _batch(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            items,
            fn_key,
            fn_proc,
            overwrite_by_pkeys=None):
        try:
            table = self.helper.web.aws.dynamodb.table.get(
                access_key_id=access_key_id,
                secret_access_key=secret_access_key,
                region_name=region_name,
                table_name=table_name)

            if not table:
                return False

            with table.batch_writer(overwrite_by_pkeys=overwrite_by_pkeys) as batch:
                fn_proc = getattr(batch, fn_proc)

                for item in items:
                    fn_proc(**{fn_key: item})

            return True

        except Exception as e:
            self.logging.exception(e)

            return False

    def _payloadize(self, payload):
        output = {}

        for k, v in payload.items():
            if v is None:
                output[k] = {'NULL': v}  # A Null data type.
            elif v is True or v is False:
                output[k] = {'BOOL': v}  # A Boolean data type.
            elif self.helper.misc.type.check.numeric(v):
                output[k] = {'N': str(v)}  # A Number data type.
            elif self.helper.misc.type.check.string(v):
                output[k] = {'S': str(v)}  # A String data type.
            elif self.helper.misc.type.check.dict(v):
                output[k] = {'L': self._payloadize(v)}  # A List of attribute values.
            elif self.helper.misc.type.check.array(v):
                tk = 'NS'  # A Number Set data type.

                for e in v:
                    if self.helper.misc.type.check.string(e):
                        tk = 'SS'  # A String Set data type.

                output[k] = {tk: [str(e) for e in v]}
            else:
                output[k] = {'S': str(v)}

        return output
