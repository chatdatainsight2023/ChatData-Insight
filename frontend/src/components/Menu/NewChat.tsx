import React from 'react';
import { useTranslation } from 'react-i18next';
import useStore from '@store/store';

import PlusIcon from '@icon/PlusIcon';

import useAddChat from '@hooks/useAddChat';

const NewChat = () => {
  const { t } = useTranslation();
  const addChat = useAddChat();
  const generating = useStore((state) => state.generating);
  const setError = useStore((state) => state.setError);

  return (
    <div className='border-t text-sm text-zinc-500 shrink-0 px-4 py-2 flex justify-between items-center gap-3'>
      <button
        type='button'
        onClick={() => {
          if (!generating) { setError(''); addChat() };
        }}
        className='h-6 w-full inline-flex items-center whitespace-nowrap justify-start bg-transparent hover:text-black'
      >
        <PlusIcon /> New Chat
      </button>
      <div className='flex items-center'>
        <button
          type='button'
          className='inline-flex items-center hover:text-black outline-none'
          aria-haspopup='menu'
          aria-expanded='false'
          data-state='closed'
        >
          <span className='i-tabler-dots'></span>
        </button>
      </div>
    </div>
  );
};

export default NewChat;
