import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx(styles.heroMinimal)}>
      <div className="container">
        <Heading as="h1" className={styles.title}>
          {siteConfig.title}
        </Heading>
        <p className={styles.subtitle}>{siteConfig.tagline}</p>
        <div className={styles.quicklinks}>
          <Link className="button button--secondary button--sm" to="/docs/intro">Start</Link>
          <Link className="button button--secondary button--sm" to="/docs/spec">Spec</Link>
          <Link className="button button--secondary button--sm" to="/blog">Changelog</Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout title={siteConfig.title} description="Physical AI Humanoid Robotics platform documentation">
      <HomepageHeader />
      <main>
        <section className="container" style={{paddingTop: '1rem', paddingBottom: '2rem'}}>
          <div className="callout-grid callout-grid--3col">
            <div className="thin-card" style={{padding: '12px'}}> 
              <h3>Architecture</h3>
              <p>System overview across sensors, actuation, perception, cognition.</p>
              <Link to="/docs/chapter-1" className="button button--secondary button--sm">Open</Link>
            </div>
            <div className="thin-card" style={{padding: '12px'}}> 
              <h3>Hardware</h3>
              <p>Actuators, sensors, compute, power, communication bus.</p>
              <Link to="/docs/chapter-2" className="button button--secondary button--sm">Open</Link>
            </div>
            <div className="thin-card" style={{padding: '12px'}}> 
              <h3>Software</h3>
              <p>Control loops, perception stack, AI logic, safety and testing.</p>
              <Link to="/docs/chapter-3" className="button button--secondary button--sm">Open</Link>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
