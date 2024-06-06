import configDev from '@/config/config.dev.json';
import configProd from '@/config/config.json';

var globalConfig = null;

export default {
    getConfig: () => {
        if (globalConfig) {
            return globalConfig;
        }
        if (process.env.NODE_ENV === 'development') {
            globalConfig = configDev;
        }
        else {
            globalConfig = configProd;
        }
        return globalConfig;
    }
}
