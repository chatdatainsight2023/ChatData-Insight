import LogoIcon from '@icon/LogoIcon';
import HomeBG from '@src/assets/background.png';
import ChatDataInsight from '@src/assets/ChatDataInsight1.png';
import Title from '@src/assets/title1.png';
import Desc from '@src/assets/desc1.png';

export default function name() {
  const goToBeta = () => {
    window.location.href = 'https://forms.gle/VXmvY3S7yN7torWT8';
  };
  return (
    <div className='bg-white min-h-screen flex flex-col'>
      <div className='flex items-center justify-between'>
        <div className='flex items-center pt-7'>
          <div className='sm:w-20 mr-7 ml-10 w-16'>
            <LogoIcon />
          </div>
          <div className='text-homeMain font-urbanist text-3xl font-extrabold'>
            <img className="sm:w-60 w-40" src={ ChatDataInsight} />
          </div>
        </div>
      </div>
      <div className='flex-grow bg-HomeBG sm:bg-[length:65%] bg-[length:100%] bg-no-repeat bg-right-bottom'>
        <div className='min-h-full sm:pt-32 pt-16'>
          <div className='font-urbanist text-6xl text-left font-blob sm:pb-14 sm:pl-24 pb-10 pl-8'>
          <img className="sm:h-56 h-28" src={ Title } />
          </div>
          <div className='font-urbanist text-3xl text-left font-medium	sm:pb-24  sm:pl-24 pb-10 pl-8'>
          <img className="sm:h-20 h-10" src={ Desc } />
          </div>
          <div className='sm:pl-24 pl-8'>
            <button onClick={goToBeta} className='text-white font-semibold	 sm:text-3xl text-lg rounded-2xl bg-gradient-to-l from-btnStart to-btnEnd px-14 py-2'>
              Join Beta
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
