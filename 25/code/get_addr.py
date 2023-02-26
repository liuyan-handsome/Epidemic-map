def get_addr():
    from selenium import webdriver
    options = webdriver.ChromeOptions()  # 必须要通过option设置浏览器的位置
    # options设置chrome位置

    options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # options.binary_location
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get("https://mp.weixin.qq.com/s/SIuDbITNdgWwYyM3eiyrgg")
    section = browser.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div[1]/div/div[1]/div[3]/section[4]/section/section/section')

    li = section.find_elements_by_tag_name('p')
    lenf = len(li)
    num = 30
    addr_name = []

    while num < lenf:
        target = li[num].find_element_by_tag_name('span')  # 需要将滚动条拖动至的指定的元素对象定位
        browser.execute_script("arguments[0].scrollIntoView();", target)
        for i in range(num - 29, num + 1):
            addr_name.append(li[i].text[:-1])
        num = num + 30
    target = li[-1].find_element_by_tag_name('span')  # 需要将滚动条拖动至的指定的元素对象定位
    browser.execute_script("arguments[0].scrollIntoView();", target)
    for i in range(num - 29, lenf - 2):
        addr_name.append(li[i].text[:-1])
    addr_name.remove("")
    browser.quit()
    return addr_name

