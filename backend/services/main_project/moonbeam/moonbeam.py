
from llama_index import StorageContext, load_index_from_storage

from services.main_project.moonbeam.embedding import establish_knowledge_base_index

def moonbeam_query_engine(question):

      # print("got moonbeam question:",question)
      
      index_folder_path = 'services/main_project/moonbeam/static/index'

    # rebuild storage context
      storage_context = StorageContext.from_defaults(persist_dir=index_folder_path)
      # load index
      index = load_index_from_storage(storage_context)

      # print("index:",index)

      query_engine = index.as_query_engine()
      response = query_engine.query(question)

      print("moonbeam query result:",response.response)

      return response.response


# establish_knowledge_base_index()



