export interface Status{
    id: number,
    name: string,
    description: string,
}

export const null_Status: Status = {
    id: null,
    name: null,
    description: null
}

export const STATUS_STATE = {
    submitted: 1,
    reviewed: 2,
    change: 3,
    approved: 4,
    denied: 5,
    expired: 6
}