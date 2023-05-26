// export type IpData = Partial<{
//     status: string;
//     country: string;
//     countryCode: string;
//     region: string;
//     regionName: string;
//     city: string;
//     zip: string;
//     lat: number;
//     lon: number;
//     timezone: string;
//     isp: string;
//     org: string;
//     as: string;
//     query: string;
// }>;

// // 懒人写法，弊端导致编辑器无法提示字段异常
// export type IpData = {
//     [key: string]: string;
// };

export interface Welcome {
    code:     string;
    data:     Data;
    charge:   boolean;
    msg:      string;
    ip:       string;
    coordsys: string;
}

export interface Data {
    continent: string;
    country:   string;
    zipcode:   string;
    timezone:  string;
    accuracy:  string;
    owner:     string;
    isp:       string;
    source:    string;
    areacode:  string;
    adcode:    string;
    asnumber:  string;
    lat:       string;
    lng:       string;
    radius:    string;
    prov:      string;
    city:      string;
    district:  string;
}
