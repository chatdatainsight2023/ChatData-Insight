from services.main_project.ethereum.eth_agent import eth_agent

def onchain_info_agent(question:str):
    
    result = eth_agent(question)

    return result