import React from 'react';
import type {Props} from '@theme/Root';
import ChatWidget from '@site/src/components/ChatWidget';

export default function Root({children}: Props) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
