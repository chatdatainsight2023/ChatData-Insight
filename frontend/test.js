{"state":{"chats":[{"title":"New Chat","messages":[{"role":"system","content":"I am powered by GPT web3 data analytics tools will disrupt the blockchain industry by breaking the paradigm of traditional data analytics methods. By providing a user-centric, efficient, and customizable solution, we enable individuals and organizations to gain a deeper understanding of the web3 ecosystem, fostering innovation and growth in the blockchain space."},{"role":"user","content":"What is the balance of address 0xc9aFcADA34d61bfBD85Db836FCb310bf66871131"},{"role":"assistant","content":"The balance of address 0xc9aFcADA34d61bfBD85Db836FCb310bf66871131 is 2ETH"},{"role":"user","content":"Please check the address: 0xc9aFcADA34d61bfBD85Db836FCb310bf66871131, the last 1 month balance change?"},{"role":"assistant","content":"Your account has had 3 transfer transactions in the last month and your account balance has increased by 0.5 ETH"},{"role":"user","content":"How much you earn today and how much you spend"},{"role":"assistant","content":"Today's income is 1.5 ETH, and expenses are 0.1 ETH"}],"config":{"model":"gpt-3.5-turbo","max_tokens":4000,"temperature":1,"presence_penalty":0,"top_p":1,"frequency_penalty":0},"titleSet":false}],"currentChatIndex":0,"apiKey":"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","apiEndpoint":"https://api.openai.com/v1/chat/completions","theme":"light","autoTitle":false,"prompts":[{"id":"0d3e9cb7-b585-43fa-acc3-840c189f6b93","name":"English Translator","prompt":"I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations. Do you understand?"}],"defaultChatConfig":{"model":"gpt-3.5-turbo","max_tokens":4000,"temperature":1,"presence_penalty":0,"top_p":1,"frequency_penalty":0},"defaultSystemMessage":"I am powered by GPT web3 data analytics tools will disrupt the blockchain industry by breaking the paradigm of traditional data analytics methods. By providing a user-centric, efficient, and customizable solution, we enable individuals and organizations to gain a deeper understanding of the web3 ecosystem, fostering innovation and growth in the blockchain space.","hideMenuOptions":false,"firstVisit":true,"hideSideMenu":false,"foldersName":[],"foldersExpanded":[]},"version":1}

const a = {
  state: {
    chats: [
      {
        title: 'New Chat 1',
        messages: [
          {
            role: 'system',
            content:
              "I am powered by GPT web3 data analytics tools will disrupt the blockchain industry by breaking the paradigm of traditional data analytics methods. By providing a user-centric, efficient, and customizable solution, we enable individuals and organizations to gain a deeper understanding of the web3 ecosystem, fostering innovation and growth in the blockchain space.",
          },
          { role: 'user', content: 'What is the balance of address 0xc9aFcADA34d61bfBD85Db836FCb310bf66871131' },
          { role: 'assistant', content: 'The balance of address 0xc9aFcADA34d61bfBD85Db836FCb310bf66871131 is 2ETH' },
          { role: 'user', content: 'Please check the address: 0xc9aFcADA34d61bfBD85Db836FCb310bf66871131, the last 1 month balance change?' },
          { role: 'assistant', content: 'Your account has had 3 transfer transactions in the last month and your account balance has increased by 0.5 ETH' },
          { role: 'user', content: 'How much you earn today and how much you spend' },
          { role: 'assistant', content: 'Today's income is 1.5 ETH, and expenses are 0.1 ETH' },
        ],
        config: {
          model: 'gpt-3.5-turbo',
          max_tokens: 4000,
          temperature: 1,
          presence_penalty: 0,
          top_p: 1,
          frequency_penalty: 0,
        },
        titleSet: false,
      },
    ],
    currentChatIndex: 0,
    apiKey: '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',
    apiEndpoint: 'https://api.openai.com/v1/chat/completions',
    theme: 'light',
    autoTitle: false,
    prompts: [
      {
        id: '0d3e9cb7-b585-43fa-acc3-840c189f6b93',
        name: 'English Translator',
        prompt:
          'I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations. Do you understand?',
      },
    ],
    defaultChatConfig: {
      model: 'gpt-3.5-turbo',
      max_tokens: 4000,
      temperature: 1,
      presence_penalty: 0,
      top_p: 1,
      frequency_penalty: 0,
    },
    defaultSystemMessage:
      "Yous  are ChatGPT, a large language model trained by OpenAI.\nCarefully heed the user's instructions. \nRespond using Markdown.\n\nhere is the question:\n",
    hideMenuOptions: false,
    firstVisit: true,
    hideSideMenu: false,
    foldersName: [],
    foldersExpanded: [],
  },
  version: 1,
};
比如，要回答几个基本问题：
1. 哪个地址的nonce最高？
2. 地址0xc9aFcADA34d61bfBD85Db836FCb310bf66871131的余额是多少？
3. 今天地址XX的收入多少，支出多少？


我想，我们一方面要实现这种最基础的，另一方面，要做longchain里，mapreduce拆分，回答的问题：
1. 请告诉我，最近1个月，以太坊上最活跃的Top10 DAPP；
2. 请告诉我，XX DAPP与哪些区块链交互最多；
3. 地址：XX，最喜欢在几点进行交易；
以上3个问题，并不是SQL就能解决。必须要多轮prompt迭代，而chatGPT是去年11月才发布。Blocktrace技术，可能不基于chatGPT


前端：输入对话框；
中间1层（自然语言）：把GPT API作为主脑，利用prompt告知它，我们后端API配置，比如，查询价格API、发送邮件API；（这些API都由chatGPT自己写）
中间2-A层（代码容器）：接收GPT结果，通过以代码形式，按照代码，比如SQL或python或shell代码，自动执行调用；
中间2-B层（记忆存储）：负责存储用户一些信息，包括周期查询prompt；
中间3层：GraphQL统一接口、API服务接口
后端：数据集、API服务



Q&A：
Q1：我的地址A：资产总价值是多少？
（数据集+交易所价格API）

Q2：上个月我的资产价值有何变化？
（GraphQL+交易所API）

Q3：上个季度DAPP X的总交易量是多少？DAPP X 在过去一个月内获得了多少新用户？
（GraphQL）

Q4：写下项目 Y 在去年的关键里程碑和成就的摘要？
（多轮prompt输入迭代+GraphQL）

Q5：分析合约 Z 代码中的安全风险？总结合约Z的主要功能？
（etherscan 合约获取API + 多轮prompt输入迭代）

Q6：我的地址收到超过 5 个 ETH 时通知我；代币 A 的价格超过 100 美元时提醒我。
（多轮prompt输入迭代 + 发送邮件API）


常见问题：
1. 请查询地址：XXX，我拥有哪些Token？
2. 请查询地址：0xc9aFcADA34d61bfBD85Db836FCb310bf66871131，我拥有哪些NFT？
3. 请查询地址：XXX，最近1个月的余额变化？
4. 请查询地址：XXX使用情况？（持有哪些Token，gas多少，发过几笔tx）



常见问题：
1. 请查询地址：XXX，我拥有哪些Token？

query BoredApe1($address: String!) {
  ethereum {
    walletByAddress(address: $address) {
      tokenBalances {
        totalCount
        edges {
          node {
            contractAddress
            totalBalance
            contract {
              name
              symbol
              decimals
            }
          }
        }        
      }
    }
  }
}


2. 请查询地址：，我拥有哪些NFT？

query BoredApe1($address: String!) {
  ethereum {
    walletByAddress(address: $address) {
      walletNFTs {
        totalCount
        edges {
          node {
            nft {
              name
              tokenId
              description
              contract {
                address
                name
                symbol
              }
            }
          }
        }
      }
    }
  }
}


3. 请查询地址：XXX，最近1个月的余额变化？=>这个可能现在查不了，没有接口查一个月前的eth余额，现在都是实时的数据

4. 请查询地址：XXX使用情况？（持有哪些Token，gas多少，发过几笔tx）
=》这个是汇总吧.另外graphql没有聚合查询，无法计算sum(gas) 
包含1（请查询地址：XXX，我拥有哪些Token？）在内
使用过的gas总和发过交易的总和query BoredApe1($address: String!) {
  ethereum {
    walletByAddress(address: $address) {
      tokenBalances {
        totalCount
        edges {
          node {
            contractAddress
            totalBalance
            contract {
              name
              symbol
              decimals
            }
          }
        }        
      }
      transactions {
        totalCount
        edges {
          node {
            gas
          }
        }
      }
    }
  }
}