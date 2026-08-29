# SUBMISSION \- Exit Exam MVC 1/2569 (เสาร์เช้า)

## 1\. วิธีเปิดโปรแกรม

- ภาษา/เฟรมเวิร์ก: Python 3  
- Entry point / คำสั่งเปิดโปรแกรม: python main.py  
- หมายเหตุที่จำเป็น (ถ้ามี):

## 2\. ตารางเชื่อมโยง Requirements

| Requirement | Model / Domain | Controller / Action | View / Screen |
| :---- | :---- | :---- | :---- |
| R1 | Judge, Contestant, Decision | ContestController | EntryView, ResultView |
| R2 | Contestant.judge\_by, Decision | ContestController.submit\_decision() | EntryView.submit\_decision() |
| R3 | Contestant.status, Contestant.decisions | ContestController.submit\_decision() | ResultView.display\_summary() |
| R4 | Judge.has\_used\_golden\_buzzer, Contestant.golden\_buzzer\_by | ContestController.use\_golden\_buzzer() | EntryView.use\_golden\_buzzer() |
| R5 | Contestant.status, Contestant.golden\_buzzer\_by | ContestController.get\_summary() | ResultView.display\_summary() |

## 3\. ผลการทดสอบ

| กรณี | ผ่าน/ไม่ผ่าน | หมายเหตุ (เฉพาะที่จำเป็น) |
| :---- | :---- | :---- |
| T1 | ผ่าน |  |
| T2 | ผ่าน |  |
| T3 | ผ่าน |  |
| T4 | ผ่าน |  |
| T5 | ผ่าน |  |
| T6 | ผ่าน |  |

## 4\. ความแตกต่างระหว่างแบบที่ออกกับโปรแกรมจริง (ถ้ามี)

1. ใน Class Diagram ไม่ได้แสดง Field “judge\_by” (เก็บรายชื่อกรรมการที่เคยตัดสินคนนั้นแล้ว) เพราะเป็นรายละเอียดภายในของ Contestant แต่ในโปรแกรมจริง จำเป็นต้องมี Field นี้ เพื่อตรวจสอบการให้ผลซ้ำ

## 5\. บันทึกการใช้ Generative AI

หากไม่ได้ใช้ ให้ระบุ **ไม่ได้ใช้ Generative AI**

| เวลาโดยประมาณ | เครื่องมือ | ใช้เพื่ออะไร | นำคำแนะนำไปใช้อย่างไร |
| :---- | :---- | :---- | :---- |
| 9.40 น. | Claude AI | สอบถามว่าตรงความสัมพันธ์ของ Class Diagram ใช้เป็นหัวลูกศรแบบเดียวกันทั้งหมด แทนลูกศรความสัมพันธ์แบบ Association, Inheritance, Realization, Dependency, Aggregation และ Composition ได้หรือไม่ เพื่อแสดง Class Diagram แบบอย่างง่าย (ไม่คำนึงถึงความถูกต้องของสัญลักษณ์ UML) | เข้าใจหลักการ แล้วนำหัวลูกศรแบบเดียวกันทั้งหมดมาใช้งาน |
| 11.00 น. | Claude AI | รันโปรแกรมแล้วเจอ TypeError: '\<' not supported between instances of 'str' and 'NoneType' จึงสอบถามว่า Error นี้เกิดจากอะไร | เข้าใจสาเหตุว่ามาจากการเทียบค่า None แล้วกลับไปแก้เงื่อนไขใน Code |
| 11.30 น. | Claude AI | ทดสอบแล้ว T3 ไม่ผ่าน จึงสอบถามแนวทางว่าควรเริ่มไล่ Debug จากจุดไหนก่อน | ได้แนวทางว่าให้ Print สถานะ Contestant ตามแต่ละ Decision  |

