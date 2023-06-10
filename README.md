# SSRF Bypass Whitelist & Blacklist
## Tổng quan kịch bản 
- Ứng dụng có chức năng đọc các note do chúng ta chọn bằng cách gửi lựa chọn của chúng ta với request POST có tham số trong phần thân của request `text = http://localhost:80/<note>`.
- Ứng dụng có một admin note chứa flag ta cần lưu trữ ở hện thống backend `http://localhost:2002/admin`.
- Với 2 version là WhiteNotion sử dụng cơ chế whitelist và BlackNotion sử dụng cơ chế blacklist để chống lỗ hỏng SSRF.
- Mục tiêu của chúng ta là bypass các cơ chế trên và đọc được `admin note` tại hệ thống `backend`.
## Kiến thức cần biết 
1. Lỗ hỏng SSRF là gì ?
> `SSRF (Server-side request forgery)` một lỗ hổng bảo mật web cho phép kẻ tấn công khiến ứng dụng phía máy chủ thực hiện các yêu cầu HTTP tới một máy chủ tùy ý do attacker lựa chọn.
3. Whitelist là gì?
>Trong cơ chế này, danh sách các nguồn tài nguyên hợp lệ được xác định trước và chỉ những yêu cầu tới các nguồn này được cho phép. Bất kỳ yêu cầu nào tới các nguồn không có trong danh sách trắng sẽ bị chặn. Danh sách này có thể được định nghĩa bằng các URL, IP, hoặc các thông tin khác liên quan đến nguồn tài nguyên.

5. Blacklist là gì?
> Trái ngược với whitelist, cơ chế blacklist cố gắng xác định các nguồn tài nguyên bị cấm và chặn bất kỳ yêu cầu nào tới chúng. Danh sách các nguồn tài nguyên bị cấm có thể bao gồm các URL, IP hoặc các thuộc tính khác của yêu cầu. Tất cả các yêu cầu tới các nguồn không có trong danh sách đen sẽ được cho phép.
7. Cách bypass 2 cơ chế trên.
> Một số ứng dụng sử dụng `blacklist` chặn đầu vào có chứa tên máy chủ như `127.0.0.1` và `localhost` hoặc các URL nhạy cảm như `/admin`. Trong tình huống này, ta có nhiều cách bypass blacklist như 
> - Sử dụng IP thay thế `127.0.0.1` chẳng hạn như `2130706433`, `017700000001` hoặc `127.1`.
> - Đăng ký tên miền của riêng bạn có độ phân giải thành `127.0.0.1`
> - Cung cấp một URL mà bạn kiểm soát, URL này sau đó sẽ chuyển hướng đến target URL

> Một số ứng dụng sử dụng `whitelist` chỉ cho phép đầu vào khớp với nội dung bắt đầu bằng `abcxyz...` hoặc nội dung chứa `abcxyz...` với `abcxyz...` là các giá trị được phép. Trong tình huống này, ta có thể khai thác sự không nhất quán trong phân tích cú pháp URL
> - Ta có thể nhúng thông tin đăng nhập vào URL trước tên máy chủ bằng cách sử dụng ký tự `@` :
> `https://expected-host:fakepassword@evil-host`
> - Ta có thể sử dụng ký tự `#` để biểu thị một URL fragment :
> `https://evil-host#expected-host`
> - Có thể tận dụng subdomain :
> `https://expected-host.evil-host`

## Setup
```
git clone https://github.com/ZioS202/SSRF_MyNotion.git
cd SSRF_MyNotion
cd WhiteNotion (hoặc BlackNotion)
docker-compose up
```

Truy cập `localhost:8000` 

## Thực hiện khai thác 
1. WhiteNotion

- Sau khi thực hiện setup xong ta có thể truy cập `localhost:8000` trên trình duyệt để quan sát giao diện trang web.

![](/img/homepage.png)

-  Tại `About` có một số hint cơ bản cho thấy rằng trang web này tồn tại lỗ hỏng SSRF và có flag tại `localhost:2002/admin`. 

![](/img/about.png)

- Ta thực hiện intercept request khi nhấn `VIEW NOTE` thì thấy rằng có tham số trong phần thân của request `text = http://localhost:80/<note>`

![](/img/viewNote1.png)

- Ta thực hiện thay đổi thành `http://localhost:2002` thì nhận được thông báo `Bạn không thể đọc note từ URL không phải là localhost:80 !!!`

![](/img/whitelistErr.png)

- Vậy ta có thể thử bypass whitelist này bằng payload sử dụng ký tự `#` để biểu thị một URL fragment : `http://localhost:2002#localhost:80/`. Và kết quả cho thấy rằng ta đã thành công truy cập vào được `backend`.

![](/img/adminBackend.png)

- Bây giờ ta chỉ cần truy cập vào endpoint `/admin` để có thể đọc flag. 

![](/img/flagWhitelist.png)

- Phân tích code cho thấy rằng cơ chế whitelist này quá đơn giản, nó chỉ kiểm tra trong url có tồn tại `localhost:80` hay không. Vậy nên payload trên của chúng ta rất dễ bypass được.

```
@app.route('/', methods=['POST'])
@app.route('/home', methods=['POST'])
def go_to():
	url = request.form.get('text')		
	if 'localhost:80' in url:
		return urllib.request.urlopen(url).read()
	else:
		logo_path = url_for ('static', filename= 'images/logo.png')
		bg_path = url_for ('static', filename= 'images/bg.webp')
		infor_mess = 'Bạn không thể đọc note từ URL không phải là localhost:80 !!!'
		return render_template('infor.html', title='Information',infor_mess=infor_mess,logo_path=logo_path,bg_path=bg_path)
```

1. BlackNotion

- Tương tự như ở trên ta thực hiện thay đổi thành `http://localhost:2002` để quan sát thì thấy rằng `Bạn không thể truy cập vào localhost !!!`

![](/img/blacklistErr.png)

- Có thể thấy rằng chương trình đã chặn localhost. Vậy ta thử payload `http://127.0.0.1:2002` và kết quả giống hệt ở trên. Vậy chương trình chặn thêm `127.0.0.1`.
- Thử thực hiện dùng `2130706433` để thay thế cho `127.0.0.1` thì có thể thấy rằng ta đã có thể bypass được hệ thống.

![](img/adminBackend.png)

- Bây giờ truy cập vào `/admin` để lấy flag tuy nhiên thì lại hiện thông báo `Bạn không thể truy cập vào admin note !!!`. Có thể chương trình đã chặn endpoint này.

![](/img/blacklistErr2.png)

-  Ta bypass bằng cách double URL-encode ký tự `a` ta đưcoj payload như sau `http://2130706433:2002/%25%36%31dmin`, quan sát thì có thể thấy rằng ta đã thành công lấy được flag.

![](/img/flagBlacklist.png)

## Biện pháp khắc phục

- Về cơ bản thì ta có thể thay đổi hành động của menu dropdown bằng cách thực hiện một request POST tới một endpoint cụ thể (thay vì một địa chỉ URL tùy ý được truyền qua tham số).

- Tiếp theo ta nên sử dụng cơ chế whitelist để kiểm tra chống lỗi SSRF. Tuy nhiên cơ chế whitelist của chúng ta cần phải code một cách hợp lý, quản lý chặt chẽ và cập nhật thường xuyên để đảm bảo rằng các nguồn tài nguyên hợp lệ không bị bỏ sót hoặc không bị attacker bypass dễ dàng như trên.
