export interface SIN{
    id: number,
    sin_number: string,
    status_id: number,
    user_id: number,
    sin_description: string,
    sin_title: string
}

export interface SINArray{
    meta: {
        results: number
    },
    SINS: SIN[]
}