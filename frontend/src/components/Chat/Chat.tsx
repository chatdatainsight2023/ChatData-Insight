import React from 'react';
import ChatContent from './ChatContent';
import ChatHeader from './ChatHeader';
const Chat = () => {

  return (
    <div className={`flex h-full flex-1 flex-col md:pl-80`}>
      <ChatHeader/>
      <main className='relative h-full w-full transition-width flex flex-col overflow-hidden items-stretch flex-1 pt-12'>
        <ChatContent />
      </main>
    </div>
  );
};

export default Chat;
