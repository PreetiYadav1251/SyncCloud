// import styles from "./page.module.css";

// export default function Home() {
//   return (
//     <main className={styles.container}>
//       <nav className={styles.navbar}>
//         <div className={styles.logo}>
//           <span className={styles.logoIcon}>☁</span>
//           <span>SyncCloud</span>
//         </div>

//         <div className={styles.navLinks}>
//           <a href="#">Home</a>
//           <a href="#">Clouds</a>
//           <a href="#">Transfers</a>
//           <a href="#">About</a>
//         </div>

//         <div className={styles.navActions}>
//           <button className={styles.loginButton}>Log in</button>
//           <button className={styles.signupButton}>Get Started</button>
//         </div>
//       </nav>

//       <section className={styles.hero}>
//         <div className={styles.heroContent}>
//           <p className={styles.badge}>☁ One place for all your clouds</p>

//           <h1>
//             Manage all your
//             <span> cloud storage </span>
//             in one place.
//           </h1>

//           <p className={styles.description}>
//             Connect your cloud storage accounts, manage files, and transfer
//             data between different cloud services from a single platform.
//           </p>

//           <div className={styles.heroActions}>
//             <button className={styles.primaryButton}>
//               Get Started →
//             </button>

//             <button className={styles.secondaryButton}>
//               Explore Features
//             </button>
//           </div>
//         </div>

//         <div className={styles.heroVisual}>
//           <div className={styles.cloudCard}>
//             <div className={styles.cloudIcon}>☁</div>
//             <h3>Your clouds, connected.</h3>
//             <p>Google Drive · OneDrive · Dropbox · More</p>

//             <div className={styles.storageBar}>
//               <div className={styles.storageProgress}></div>
//             </div>

//             <div className={styles.storageInfo}>
//               <span>Cloud Storage</span>
//               <span>68%</span>
//             </div>
//           </div>
//         </div>
//       </section>

//       <section className={styles.features}>
//         <div className={styles.feature}>
//           <div className={styles.featureIcon}>🔗</div>
//           <h3>Connect Clouds</h3>
//           <p>
//             Connect multiple cloud storage services to SyncCloud.
//           </p>
//         </div>

//         <div className={styles.feature}>
//           <div className={styles.featureIcon}>↔️</div>
//           <h3>Transfer Files</h3>
//           <p>
//             Move or copy files between your connected cloud accounts.
//           </p>
//         </div>

//         <div className={styles.feature}>
//           <div className={styles.featureIcon}>📁</div>
//           <h3>Manage Files</h3>
//           <p>
//             Browse, organize, rename, download and manage your files.
//           </p>
//         </div>
//       </section>
//     </main>
//   );
// }


"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

export default function Home() {
  const [backendStatus, setBackendStatus] = useState("Checking...");

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL;

        const response = await fetch(`${apiUrl}/health`);

        if (!response.ok) {
          throw new Error("Backend request failed");
        }

        const data = await response.json();

        if (data.status === "healthy") {
          setBackendStatus("Connected");
        } else {
          setBackendStatus("Not Connected");
        }
      } catch (error) {
        console.error("Backend connection error:", error);
        setBackendStatus("Not Connected");
      }
    };

    checkBackend();
  }, []);

  return (
    <main className={styles.container}>
      <nav className={styles.navbar}>
        <div className={styles.logo}>
          <span className={styles.logoIcon}>☁</span>
          <span>SyncCloud</span>
        </div>

        <div className={styles.navLinks}>
          <a href="#">Home</a>
          <a href="#">Clouds</a>
          <a href="#">Transfers</a>
          <a href="#">About</a>
        </div>

        <div className={styles.navActions}>
          <button className={styles.loginButton}>Log in</button>
          <button className={styles.signupButton}>Get Started</button>
        </div>
      </nav>

      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <p className={styles.badge}>☁ One place for all your clouds</p>

          <h1>
            Manage all your
            <span> cloud storage </span>
            in one place.
          </h1>

          <p className={styles.description}>
            Connect your cloud storage accounts, manage files, and transfer
            data between different cloud services from a single platform.
          </p>

          <p>
            Backend Status:{" "}
            <strong>
              {backendStatus === "Connected"
                ? "🟢 Connected"
                : `🟡 ${backendStatus}`}
            </strong>
          </p>

          <div className={styles.heroActions}>
            <button className={styles.primaryButton}>
              Get Started →
            </button>

            <button className={styles.secondaryButton}>
              Explore Features
            </button>
          </div>
        </div>

        <div className={styles.heroVisual}>
          <div className={styles.cloudCard}>
            <div className={styles.cloudIcon}>☁</div>

            <h3>Your clouds, connected.</h3>

            <p>Google Drive · OneDrive · Dropbox · More</p>

            <div className={styles.storageBar}>
              <div className={styles.storageProgress}></div>
            </div>

            <div className={styles.storageInfo}>
              <span>Cloud Storage</span>
              <span>68%</span>
            </div>
          </div>
        </div>
      </section>

      <section className={styles.features}>
        <div className={styles.feature}>
          <div className={styles.featureIcon}>🔗</div>

          <h3>Connect Clouds</h3>

          <p>
            Connect multiple cloud storage services to SyncCloud.
          </p>
        </div>

        <div className={styles.feature}>
          <div className={styles.featureIcon}>↔️</div>

          <h3>Transfer Files</h3>

          <p>
            Move or copy files between your connected cloud accounts.
          </p>
        </div>

        <div className={styles.feature}>
          <div className={styles.featureIcon}>📁</div>

          <h3>Manage Files</h3>

          <p>
            Browse, organize, rename, download and manage your files.
          </p>
        </div>
      </section>
    </main>
  );
}