import Link from "next/link";
import styles from "./page.module.css";

export default function RegisterPage() {
  return (
    <main className={styles.page}>
      <section className={styles.brandSection}>
        <Link href="/" className={styles.logo}>
          <span className={styles.logoIcon}>☁</span>
          <span>SyncCloud</span>
        </Link>

        <div className={styles.brandContent}>
          <p className={styles.badge}>☁ Start your journey</p>

          <h1>
            All your clouds.
            <span> One powerful platform.</span>
          </h1>

          <p>
            Create your SyncCloud account and manage your cloud storage
            services from one simple place.
          </p>
        </div>
      </section>

      <section className={styles.formSection}>
        <div className={styles.formCard}>
          <div className={styles.formHeader}>
            <h2>Create account</h2>
            <p>Get started with SyncCloud today.</p>
          </div>

          <form>
            <div className={styles.inputGroup}>
              <label htmlFor="name">Full name</label>

              <input
                id="name"
                type="text"
                placeholder="Enter your name"
                required
              />
            </div>

            <div className={styles.inputGroup}>
              <label htmlFor="email">Email</label>

              <input
                id="email"
                type="email"
                placeholder="Enter your email"
                required
              />
            </div>

            <div className={styles.inputGroup}>
              <label htmlFor="password">Password</label>

              <input
                id="password"
                type="password"
                placeholder="Create a password"
                required
              />

              <p className={styles.passwordHint}>
                Password must be at least 8 characters.
              </p>
            </div>

            <div className={styles.inputGroup}>
              <label htmlFor="confirmPassword">Confirm password</label>

              <input
                id="confirmPassword"
                type="password"
                placeholder="Confirm your password"
                required
              />
            </div>

            <button type="submit" className={styles.registerButton}>
              Create Account
            </button>
          </form>

          <div className={styles.divider}>
            <span>or</span>
          </div>

          <p className={styles.loginText}>
            Already have an account?{" "}
            <Link href="/login">Log in</Link>
          </p>
        </div>
      </section>
    </main>
  );
}