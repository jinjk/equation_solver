import configDev from '@/config/config.dev.json';
import configProd from '@/config/config.json';
export default {
    getConfig: () => {
        if (process.env.NODE_ENV === 'development') {
            return configDev
        }
        else {
            return configProd
        }
        console.log(process.env.NODE_ENV)
    }
}