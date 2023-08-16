import React, { useState, useEffect } from 'react';
import useStore from '@store/store';
import { Role } from '@type/chat';
import { useTranslation } from 'react-i18next';
import { ChatInterface } from '@type/chat';
import useSubmit from '@hooks/useSubmit';
const EditViewButtons = React.memo(
  ({
    sticky = false,
    handleSaveAndSubmit,
    handleSave,
    setIsModalOpen,
    setIsEdit,
    _setContent,
  }: {
    sticky?: boolean;
    handleSaveAndSubmit: () => void;
    handleSave: () => void;
    setIsModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
    setIsEdit: React.Dispatch<React.SetStateAction<boolean>>;
    _setContent: React.Dispatch<React.SetStateAction<string>>;
  }) => {
    const { t } = useTranslation();

    return (
      <div className='flex'>
        <div className='flex-1 text-center flex justify-center'>
          {sticky && (
            <button
              className='btn relative btn-primary'
              onClick={handleSaveAndSubmit}
            >
              <div className='flex items-center justify-center gap-2'>
                {t('saveAndSubmit')}
              </div>
            </button>
          )}

          {sticky || (
            <button
              className='btn relative btn-neutral'
              onClick={() => {
                setIsModalOpen(true);
              }}
            >
              <div className='flex items-center justify-center gap-2'>
                {t('saveAndSubmit')}
              </div>
            </button>
          )}

          {sticky || (
            <button
              className='btn relative btn-neutral'
              onClick={() => setIsEdit(false)}
            >
              <div className='flex items-center justify-center gap-2'>
                {t('cancel')}
              </div>
            </button>
          )}
        </div>
      </div>
    );
  }
);
const EditView = ({
  content,
  setIsEdit,
  messageIndex,
  sticky,
}: {
  content: string;
  setIsEdit: React.Dispatch<React.SetStateAction<boolean>>;
  messageIndex: number;
  sticky?: boolean;
}) => {
  const inputRole = useStore((state) => state.inputRole);
  const setChats = useStore((state) => state.setChats);
  const currentChatIndex = useStore((state) => state.currentChatIndex);
  const error = useStore((state) => state.error);
  const setError = useStore((state) => state.setError);

  const [_content, _setContent] = useState<string>(content);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const textareaRef = React.createRef<HTMLTextAreaElement>();

  const { t } = useTranslation();

  const resetTextAreaHeight = () => {
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.shiftKey) && e.key === 'Enter') {
      e.preventDefault();
      if (sticky) {
        handleSaveAndSubmit();
        resetTextAreaHeight();
      } else handleSave();
    }
  };

  const clickHandle = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    handleSaveAndSubmit();
    resetTextAreaHeight();
  };
  const handleSave = () => {
    if (sticky && _content === '') return;
    const updatedChats: ChatInterface[] = JSON.parse(
      JSON.stringify(useStore.getState().chats)
    );
    const updatedMessages = updatedChats[currentChatIndex].messages;
    if (sticky) {
      updatedMessages.push({ role: inputRole, content: _content });
      _setContent('');
      resetTextAreaHeight();
    } else {
      updatedMessages[messageIndex].content = _content;
      setIsEdit(false);
    }
    setChats(updatedChats);
  };

  const { handleSubmit } = useSubmit();
  const handleSaveAndSubmit = () => {
    const updatedChats: ChatInterface[] = JSON.parse(
      JSON.stringify(useStore.getState().chats)
    );
    const updatedMessages = updatedChats[currentChatIndex].messages;
    if (sticky) {
      if (_content !== '') {
        updatedMessages.push({ role: inputRole, content: _content });
      }
      _setContent('');
      resetTextAreaHeight();
    } else {
      updatedMessages[messageIndex].content = _content;
      updatedChats[currentChatIndex].messages = updatedMessages.slice(
        0,
        messageIndex + 1
      );
      setIsEdit(false);
    }
    setChats(updatedChats);
    handleSubmit(_content);
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [_content]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, []);

  return (
    <div className='fixed bottom-0 left-0 right-0 shrink-0 px-3 py-3 bg-vert-light-gradient dark:bg-vert-dark-gradient transition-transform md:ml-80'>
      {error && <div className="text-center max-w-3xl mx-auto p-2 border rounded-md	border-rose-700	text-rose-700 mb-2">{error}</div>}
      <div className='mb-2'>
        <div className='max-w-3xl mx-auto flex justify-center h-full items-center'>
          <div className='text-xs flex items-center gap-2'>
            <button
              type='button'
              className='rounded-lg px-2 text-sm inline-flex items-center justify-center border shrink-0 text-center disabled:pointer-events-none border-zinc-300 bg-white border-b-zinc-400/80 active:bg-zinc-200 h-8'
            >
              <span className='i-tabler-plus mr-[2px]'></span>New Chat
            </button>
            <button
              type='button'
              className='rounded-lg px-2 text-sm inline-flex items-center justify-center border shrink-0 text-center disabled:pointer-events-none border-zinc-300 bg-white border-b-zinc-400/80 active:bg-zinc-200 h-8'
            >
              <span className='mr-1 i-tabler-refresh'></span>Regenerate
            </button>

            <button
              type='button'
              id='radix-:rk:'
              aria-haspopup='menu'
              aria-expanded='false'
              data-state='closed'
              className='rounded-lg px-2 text-sm inline-flex items-center justify-center border shrink-0 text-center disabled:pointer-events-none border-zinc-300 bg-white border-b-zinc-400/80 active:bg-zinc-200 h-8'
            >
              <span className='i-tabler-dots'></span>
            </button>
          </div>
        </div>
      </div>
      <div className='max-w-3xl mx-auto h-full'>
        <div className='relative'>
          <div className='flex items-center h-full bg-zinc-100 rounded-xl focus-within:ring-2 ring-blue-500'>
            <textarea
              ref={textareaRef}
              className='flex-grow outline-none bg-transparent scroll-p-2 px-3 py-2 min-h-[2.6rem] rounded-xl resize-none'
              placeholder='Type message or / to select a prompt'
              onChange={(e) => {
                _setContent(e.target.value);
              }}
              value={_content}
              onKeyDown={handleKeyDown}
              rows={1}
            ></textarea>
            <div className='pr-2 inline-flex items-center'>
              <button
                type='button'
                onClick={clickHandle}
                className='h-8 w-8 hover:bg-zinc-300 rounded-xl inline-flex items-center justify-center'
              >
                <span className='i-tabler-send'></span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
const InputBar = React.memo(
  ({
    role,
    content,
    messageIndex,
    sticky = false,
  }: {
    role: Role;
    content: string;
    messageIndex: number;
    sticky?: boolean;
  }) => {
    const hideSideMenu = useStore((state) => state.hideSideMenu);
    const [isEdit, setIsEdit] = useState<boolean>(sticky);

    return (
      <div
        className={`w-full border-b border-black/10 dark:border-gray-900/50 text-gray-800 dark:text-gray-100 group`}
      >
        <div
          className={`text-sm flex transition-all justify-center bgimage ease-in-out py-3`}
        >
          <div className='w-8/12'>
            <EditView
              content={content}
              setIsEdit={setIsEdit}
              messageIndex={messageIndex}
              sticky={sticky}
            />
          </div>
        </div>
      </div>
    );
  }
);

export default InputBar;
