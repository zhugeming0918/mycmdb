from config import settings
from lib.log import Logger
import importlib
from src.asset.basic import BasicPlugin


def get_asset_entries():
    ret = dict()
    ret.update(BasicPlugin().asset)
    plugins = getattr(settings, 'PLUGINS', [])
    for plugin in plugins:
        try:
            model_path, cls_name = plugin.rsplit('.', maxsplit=1)
            cls = getattr(importlib.import_module(model_path), cls_name)
            ret.update(cls().asset)
        except Exception as e:
            Logger().error('Error no module {}: {}'.format(plugin, str(e)))
    return ret


if __name__ == '__main__':                  # TODO 仅供测试使用
    for name, info in get_asset_entries().items():
        print("{}:".format(name))
        cmd_lst, parse_method = info
        print("\t{:50} - {}".format(str(cmd_lst), parse_method))
