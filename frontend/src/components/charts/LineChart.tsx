import React, { useState, useEffect, useId } from 'react';
import ReactDOM from 'react-dom';
import Plotly from 'plotly.js-dist';

const DemoStock = ({ data }: any) => {
  const htmlId = useId();
  useEffect(() => {
    const trace1 = {
      x: data.map((d: { open_timestamp: any; }) => d.open_timestamp),
      close: data.map((d: { close: any; }) => d.close),
      decreasing: { line: { color: 'rgba(255,50,10,1)' } },
      high: data.map((d: { high: any; }) => d.high),
      increasing: { line: { color: 'rgba(31,119,180,1)' } },
      line: { color: 'rgba(31,119,180,1)' },
      low: data.map((d: { low: any; }) => d.low),
      open: data.map((d: { open: any; }) => d.open),
      type: 'candlestick',
      xaxis: 'x',
      yaxis: 'y'
    };
    const dates = data.map((d: { date: any; }) => d.date);
    const dateRange = [dates[0], dates[dates.length - 1]];
    const layout = {
      dragmode: 'zoom',
      margin: {
        r: 10,
        t: 25,
        b: 40,
        l: 60
      },
      showlegend: false,
      xaxis: {
        autorange: true,
        rangeslider: { range: dateRange },
        title: "TimeStamp",
        type: 'date'
      },
      yaxis: {
        autorange: true,
        type: 'linear'
      },
    };
    Plotly.newPlot(htmlId, [trace1], layout);
  }, [data]);
  return (
    <div id={htmlId}></div>
  )
};
export default DemoStock;