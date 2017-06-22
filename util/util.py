# encoding: utf-8


def save_docs_to_local(doc_path,doc_name,doc_context):
    import os
    basedir = os.path.abspath(os.path.dirname(__file__))
    # basedir, _ = os.path.split(basedir)

    try:
        with open(os.path.join(basedir, doc_path, doc_name).decode("utf-8"), 'w') as f:
            f.write(doc_context)
        print("保存查询网页成功。")
    except Exception as e:
        print("保存文件出现错误。"),e


