import React, { useEffect } from 'react';
import useStore from '@store/store';

import NewChat from './NewChat';
import ChatHistoryList from './ChatHistoryList';
import CrossIcon2 from '@icon/CrossIcon2';

const Menu = () => {

  return (
    <>
      <div
        id='menu'
        className={`group/menu dark fixed md:inset-y-0 md:flex md:w-80 md:flex-col transition-transform z-[999] h-full max-md:w-3/4 border-r left-0 top-0 bottom-0 bg-zinc-100`}>
        <div className='flex h-full min-h-0 flex-col'>
          <div className='scrollbar-trigger flex h-full w-full flex-1 items-start border-white/20'>
            <nav className='flex h-full flex-1 flex-col space-y-1'>
            <header className="pt-4 h-12 pb-1 flex items-center px-4 justify-between"><a href="/"><span className="font-extrabold inline-block text-transparent bg-clip-text bg-gradient-to-r from-logStart to-logEnd text-xl">ChatData Insight</span></a></header>
              <ChatHistoryList />
              <NewChat />
            </nav>
          </div>
        </div>
      </div>
    </>
  );
};

export default Menu;
