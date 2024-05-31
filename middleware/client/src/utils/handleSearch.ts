import mdwApi from "./mdwApi";


export default async function handleSearch(appName: string, query: string, ignore_fields: string[]) {
    const response = await mdwApi.post(`/search/${appName}`, {
        query,
        ignore_fields,
    });
    if (response.status === 200) {
        return response.data as any[];
    } else {
        return undefined;
    }
}