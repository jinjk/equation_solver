import appConfig from "../config/app-config";

const config = appConfig.getConfig();

export default {
    getBookInfo: async () => {
        appConfig.getConfig();
        return {
            title: '小学语文三年级下册',
            pageCount: 132
        };
    },

    findText: async (text) => {
        try {
            const result = await fetch(`${config.serviceUrl}/books/search?text=${text}`);
            return result.json();
        }
        catch (error) {
            console.error('Error:', error);
            return {
                error: error
            }
        }
    }
}
