class Tracking:
    def __init__(self, data):
        self.order_reference = data['ORDER_REFERENCE']
        self.order_status = data['ORDER_STATUS']
        self.order_statusdate = data['ORDER_STATUSDATE']
        self.order_note = data['ORDER_NOTE']
        self.mapg_ketnoi = data['MAPG_KETNOI']
        self.tra_cuu = data['TRA_CUU']
        self.trang_chu = data['TRANG_CHU']
        self.buu_cuc = data['BUU_CUC']
        self.lat = data['lat']
        self.lng = data['lng']

    def __str__(self):
        return f'{self.order_statusdate}: {self.order_note}: {self.buu_cuc}'


class TrackingOrder:
    def __init__(self, data):
        self.order_id = data['MA_KIEN']
        self.input_date = data['NGAY_NHAP']
        self.latest_status_time = data['TIME_TRANGTHAI']
        self.from_post_office = data['BUUCUC_NHAN']
        self.to_post_office = data['BUUCUC_DEN']
        self.weight = data['TRONG_LUONG']
        self.service_type = data['DICH_VU']
        self.status = data['GHI_CHU']
        self.status_code = data['MA_TRANGTHAI']
        self.trackings = []
        for tracking in data['TRACKINGS']:
            self.trackings.append(Tracking(tracking))

    def __str__(self):
        output = f'Tracking order: {self.order_id}\n'
        output += f'Weight (gram): {self.weight}\n'
        output += f'Service: {self.service_type}\n'
        output += f'Status: {self.status}\n\n'

        for tracking in self.trackings:
            output += str(tracking) + '\n'
        return output
