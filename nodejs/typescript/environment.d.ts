declare global {
    namespace NodeJS {
        interface ProcessEnv {
            DEFAULT_NAMESPACE: string;
            BROKER_NAME: string;
            BROKER_TOKEN: string;
            PUBSUB_ENDPOINT: string;
            PUBSUB_PORT: string;
        }
    }
}

export { }