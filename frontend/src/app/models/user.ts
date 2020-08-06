export interface User{
    id: number,
    email: string;
    groups: string[];
}

export const null_User : User ={
    id: null,
    email: null,
    groups: null
}