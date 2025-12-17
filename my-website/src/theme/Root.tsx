import React from 'react';
import type {Props} from '@theme/Root';
import Chatbot from '@site/src/components/Chatbot/Chatbot';

export default function Root({children}: Props) {
  return (
    <>
      {children}
      <Chatbot />
    </>
  );
}
