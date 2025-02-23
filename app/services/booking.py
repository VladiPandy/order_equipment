import datetime
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from typing import Dict, List, Any
import json

from models.schemas.booking import PossibleCreateBookingRequest, \
    PossibleCreateBookingResponse, CreateBookingResponse, \
    CreateBookingRequest, PossibleChangesResponse, PossibleChangesRequest, \
    ChoseData, ChangeData, ChangeRequest, ChangeResponse, CancelResponse, \
    CancelRequest, FeedbackResponse, FeedbackRequest


class UserBookingService:

    @staticmethod
    async def parse_date(date_str: str) -> datetime.date:
        """
        Преобразует строку в объект datetime.date, пытаясь два формата:
        - '%d-%m-%Y'
        - '%d-%m-%y'

        :param date_str: Строка с датой.
        :return: Объект datetime.date.
        :raises ValueError: Если ни один формат не подходит.
        """
        print(date_str)
        for fmt in ('%y-%m-%d','%Y-%m-%d','%d-%m-%Y', '%d-%m-%y','%d.%m.%Y', '%d.%m.%y'):
            try:
                return datetime.strptime(str(date_str), fmt).date()
            except ValueError:
                continue

    @staticmethod
    async def validate_date_booking(request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Валидирует и определяет диапазон дат для бронирования.

        Если в запросе присутствуют ключи 'start' и 'end', пытается их разобрать.
        Если их нет, то устанавливает диапазон от текущего дня - 2 недели до текущего дня + 2 недели.
        Также поддерживается вариант, когда переданы параметры 'week' и 'year'
        для расчета начала и конца недели по ISO календарю.

        :param request: Словарь с параметрами запроса.
        :return: Словарь с date_start, date_end и dates_list (список дат в формате "dd.mm.yyyy").
        :raises HTTPException: При ошибке валидации.
        """
        print('certian_date' in request)
        try:
            # Если переданы параметры start и end, пытаемся их разобрать.
            if 'start' in request and request['start']:
                try:
                    date_start = await UserBookingService.parse_date(request['start'])

                except ValueError as e:
                    raise HTTPException(status_code=400,
                                        detail=f"Ошибка формата start: {e}")

                if 'end' in request and request['end']:
                    try:
                        date_end = await UserBookingService.parse_date(request['end'])
                    except ValueError as e:
                        raise HTTPException(status_code=400,
                                            detail=f"Ошибка формата end: {e}")
                else:
                    # Если end не указан, берем диапазон 2 недели назад и 2 недели вперед от сегодня.
                    today = datetime.today().date()
                    date_start = today - timedelta(weeks=2)
                    date_end = today + timedelta(weeks=2)
            # Если параметров start/end нет, но есть week и year - используем их.
            elif 'certian_date' in request and request['certian_date']:
                try:
                    certian_date = await UserBookingService.parse_date(request['certian_date'])

                    week = certian_date.isocalendar()[1]
                    year = certian_date.isocalendar()[0]
                    date_start = datetime.fromisocalendar(year, week, 1).date()
                    date_end = datetime.fromisocalendar(year, week, 7).date()
                except Exception as e:
                    raise HTTPException(status_code=400,
                                        detail=f"Неверный формат week/year: {e}")

            elif 'week' in request and 'year' in request:
                try:
                    week = int(request['week'])
                    year = int(request['year'])
                    date_start = datetime.fromisocalendar(year, week, 1).date()
                    date_end = datetime.fromisocalendar(year, week, 7).date()
                except Exception as e:
                    raise HTTPException(status_code=400,
                                        detail=f"Неверный формат week/year: {e}")
            else:
                # Если ни start/end, ни week/year не переданы, устанавливаем диапазон по умолчанию.
                today = datetime.today().date()
                date_start = today - timedelta(weeks=2)
                date_end = today + timedelta(weeks=2)

            print(date_start)
            print(date_end)
            if date_start > date_end:
                raise HTTPException(status_code=400,
                                    detail="Дата начала не может быть позже даты окончания.")

            # Генерируем список дат в формате "dd.mm.yyyy" от date_start до date_end включительно.
            num_days = (date_end - date_start).days + 1
            dates = [
                (date_start + timedelta(days=i)).strftime("%d.%m.%Y")
                for i in range(num_days)
            ]

            return {
                'date_start': date_start,
                'date_end': date_end,
                'dates_list': dates
            }
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Ошибка валидации дат: {e}")

    @staticmethod
    async def get_uuids(db: AsyncSession,username, data) -> None:
        print(data)
        try:
            if 'date' in data:

                date_val = datetime.strptime(data['date'],
                                                      '%d.%m.%Y').date()
                date_text = f"""date = '{date_val}'"""

            else:
                date_text = '1 = 1'
                date_val = datetime.strptime('20.01.5999',
                                                      '%d.%m.%Y').date()
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Неверный формат даты: {e}")

        try:
            if 'analyse' in data:
                analyze_val = f"a.analyze_name = '{data['analyse']}'"
                analyze_info = await db.execute(text(
                    f"SELECT id FROM \"analyze\" WHERE analyze_name = '{data['analyse']}' ;"))
                analyze_id = "'" + str(analyze_info.scalars().all()[0]) + "'"
            elif 'analyze_id' in data:
                analyze_id = "'" + str(data['analyze_id']) + "'"
                analyze_name = await db.execute(text(
                    f"SELECT analyze_name FROM \"analyze\" WHERE id = {analyze_id} ;"))
                analyze_val = f"a.analyze_name = '{str(analyze_name.scalars().all()[0])}'"
            else:
                analyze_val = '1 = 1'
                analyze_id = 'NULL'
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Неверный формат анализа: {e}")

        if 'equipment' in data:
            equipment_val = f"eq.\"name\" ='{data['equipment']}'"
            equipment_info = await db.execute(text(
                f"SELECT id FROM \"equipment\" WHERE name = '{data['equipment']}' ;"))
            equipment_id = "'" + str(equipment_info.scalars().all()[0]) + "'"
        else:
            equipment_val = '1 = 1'
            equipment_id = 'NULL'

        try:
            if 'executor' in data:

                    operator_val = f"concat(ex.first_name,' ',ex.last_name,' ',ex.patronymic) = '{data['executor']}'"
                    operator_info = await db.execute(text(
                        f"SELECT id FROM \"executor\" WHERE concat(first_name,' ',last_name,' ',patronymic) = '{data['executor']}' ;"))
                    operator_id = "'" + str(operator_info.scalars().all()[0]) + "'"

            else:
                operator_val = '1 = 1'
                operator_id = 'NULL'

        except Exception as e:
            raise HTTPException(status_code=400,
                            detail=f"Неверный формат исполнителя: {e}")

        print('date' in data)
        responsible_person = await db.execute(text(
            f"SELECT id FROM \"project\" WHERE project_nick = '{username}' ;"))
        items = responsible_person.scalars().all()

        uuids_json = {
            'date_text' : date_text,
            'date_val' : date_val,
            'analyze_val' : analyze_val,
            'analyze_id' : analyze_id,
            'equipment_val': equipment_val,
            'equipment_id': equipment_id,
            'operator_val': operator_val,
            'operator_id': operator_id,
            'user_id': items[0] if items else ''
        }

        return uuids_json

    @staticmethod
    async def validate_token(db: AsyncSession, cookie_createkey: str) -> None:
        print(cookie_createkey)
        timestamp_query = text("""
            SELECT update_timestamp, write_timestamp, id_delete
            FROM public.block_booking
            WHERE cookies_key = :cookie_key
            LIMIT 1
        """)
        result = await db.execute(timestamp_query,
                                  {"cookie_key": cookie_createkey})
        row = result.fetchone()
        print(row)
        if not row:
            raise HTTPException(status_code=403, detail="Токен не найден")
        update_ts, write_ts, id_delete = row
        effective_ts = update_ts if update_ts is not None else write_ts
        print(effective_ts)
        if effective_ts is None:
            raise HTTPException(status_code=403,
                                detail="Отсутствует временная метка в токене")
        now = datetime.utcnow()
        if now - effective_ts > timedelta(minutes=5):
            await UserBookingService.block_cookie_key(db,
                                                  cookie_createkey)
            raise HTTPException(status_code=403,
                                detail="Заполнение запрещено – токен истёк")

        if id_delete:
            await UserBookingService.block_cookie_key(db,
                                                  cookie_createkey)
            raise HTTPException(status_code=403,
                                detail="Заполнение запрещено – токен заблокирован")

    @staticmethod
    async def create_new_cookie_key(db: AsyncSession, user_id: object) -> str:
        insert_query = text("""
            INSERT INTO public.block_booking
            (project_id)
            VALUES (:project_id)
            RETURNING cookies_key
        """)
        try:
            result = await db.execute(insert_query, {
                "project_id": user_id
            })
            new_cookie_key = result.scalar()
            await db.commit()
            return new_cookie_key
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500,
                                detail=f"Ошибка при создании токена: {e}")

    @staticmethod
    async def block_cookie_key(db: AsyncSession, cookie_createkey: object) -> None:

        block_token_query = text(f"""
                                UPDATE public.block_booking
                                SET update_timestamp = now(),
                                    id_delete = True
                                WHERE cookies_key = '{cookie_createkey}'
                            """)
        try:
            result = await db.execute(block_token_query)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500,
                                detail=f"Ошибка при блокировки токена: {e}")

    @staticmethod
    async def update_blocking_period(db: AsyncSession,
                                    uuids_json,
                                    cookie_createkey) -> None:

        update_query = text(f"""
                                UPDATE public.block_booking
                                SET 
                                    date_booking = '{uuids_json['date_val']}',
                                    analyse_id = {uuids_json['analyze_id']},
                                    equipment_id = {uuids_json['equipment_id']},
                                    executor_id =  {uuids_json['operator_id']},
                                    update_timestamp = now()
                                WHERE cookies_key = '{cookie_createkey}'
                            """)
        try:
            result = await db.execute(update_query)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500,
                                detail=f"Ошибка при обновлении записи: {e}")

    @staticmethod
    async def availible_values(db: AsyncSession,
                                     uuids_json,
                                     date_booking_dict,
                                     blocking_element
                                ) -> None:
        new_values_query = text(f"""
                             with  days_employes as (
                                SELECT 1 d, x.executor_id  FROM public.control_enter_workerweekstatus x
                                where x.monday = 'Работает' 
                                union all 
                                SELECT 2 d, x.executor_id  FROM public.control_enter_workerweekstatus x
                                where x.tuesday = 'Работает' 
                                union all 
                                SELECT 3 d, x.executor_id  FROM public.control_enter_workerweekstatus x
                                where x.wednesday = 'Работает' 
                                union all 
                                SELECT 4 d, x.executor_id  FROM public.control_enter_workerweekstatus x
                                where x.thursday = 'Работает' 
                                union all 
                                SELECT 5 d, x.executor_id  FROM public.control_enter_workerweekstatus x
                                where x.friday = 'Работает'
                                union all 
                                SELECT 6 d, x.executor_id  FROM public.control_enter_workerweekstatus x
                                where x.saturday = 'Работает' 
                                union all 
                                SELECT 7 d, x.executor_id  FROM public.control_enter_workerweekstatus x
                                where x.sunday = 'Работает' 
                                )
                                ,days_working as
                                (
                                SELECT 1 d FROM public.control_enter_workingdayofweek x
                                where x.monday = true
                                union all 
                                SELECT 2 d FROM public.control_enter_workingdayofweek x
                                where x.tuesday = true
                                union all 
                                SELECT 3 d FROM public.control_enter_workingdayofweek x
                                where x.wednesday = true
                                union all 
                                SELECT 4 d FROM public.control_enter_workingdayofweek x
                                where x.thursday = true
                                union all 
                                SELECT 5 d FROM public.control_enter_workingdayofweek x
                                where x.friday = true
                                union all 
                                SELECT 6 d FROM public.control_enter_workingdayofweek x
                                where x.saturday = true
                                union all 
                                SELECT 7 d FROM public.control_enter_workingdayofweek x
                                where x.sunday = true
                                )
                                ,executor_limit as (
                                    select executor_id  ,sum(count_analyses) used_limit, count(count_analyses) count_executor_per_day
                                    from projects_booking
                                    where date_booking between '{date_booking_dict['date_start']}'::date 
                                        and '{date_booking_dict['date_end']}'::date and (is_delete = False or status != 'Отклонено')
                                    group by date_booking, executor_id 
                                )
                                ,equipment_limit as (
                                    select equipment_id   ,sum(count_analyses) used_limit, count(count_analyses) count_equipment_per_day
                                    from projects_booking
                                    where date_booking between '{date_booking_dict['date_start']}'::date 
                                        and '{date_booking_dict['date_end']}'::date and (is_delete = False or status != 'Отклонено')
                                    group by date_booking, equipment_id 
                                )
                                ,used_limits_analese_equipment as (
                                    select analyse_id ,equipment_id ,sum(count_analyses) used_limit
                                    from projects_booking
                                    where {blocking_element} project_id = '{uuids_json['user_id']}' and
                                         date_booking between '{date_booking_dict['date_start']}'::date 
                                        and '{date_booking_dict['date_end']}'::date and (is_delete = False or status != 'Отклонено')
                                    group by analyse_id ,equipment_id 
                                )
                                ,blocking_list as
                            (
                                select *
                                from block_booking
                                where write_timestamp+'10 minutes'::interval > now()  
                                       {blocking_element} and project_id != '{uuids_json['user_id']}'
                                        and id_delete = False
                            )
                            SELECT 
                                distinct 
                                date::DATE AS fact_date
                                ,y.project_name 
                                , y.id
                                , a.analyze_name
                                , eq."name" 
                                , eq.status 
                                , concat(ex.first_name,' ',ex.last_name,' ',ex.patronymic) fio_x
                                , x.limit_samples - coalesce(ul.used_limit,0) limit_samples
                                , x.limit_samples limits_per_eq
                                , coalesce(ul.used_limit,0)
                                , eql.count_equipment_per_day
                                , exl.count_executor_per_day
                                , z.analazy_id::text
                                , v.equipment_id::text
                                , v.operator_id::text
                            FROM generate_series(
                                DATE '{date_booking_dict['date_start']}'::date, -- Начальная дата
                                DATE '{date_booking_dict['date_end']}'::date, -- Конечная дата
                                INTERVAL '1 day'   -- Шаг (1 день)
                            ) AS t(date)
                            left join  project y on 1=1
                            right join dependings_projectperanalyze x on x.project_n_id = y.id 
                            left join dependings_analyzeperequipment z on z.analazy_id = x.analazy_n_id 
                            left join dependings_operatorperequipment v on v.equipment_id = z.equipment_name_id 
                            left join "analyze" a on a.id  = z.analazy_id 
                            left join equipment eq on eq.id  = v.equipment_id 
                            left join executor ex on ex.id = v.operator_id 
                            left join blocking_list bl on  case 
                                when coalesce(bl.equipment_id,bl.analyse_id) is null  then  bl.date_booking = date::DATE and  bl.executor_id = v.operator_id
                                when coalesce(bl.analyse_id,bl.equipment_id,bl.executor_id) is null and bl.date_booking is null then  1 = 2
                                when coalesce(bl.equipment_id,bl.executor_id) is null and bl.date_booking is null and bl.analyse_id  is not null then  bl.analyse_id = z.analazy_id 
                                when coalesce(bl.analyse_id,bl.equipment_id,bl.executor_id) is null and bl.date_booking is not null   then  bl.date_booking = date::DATE
                                when coalesce(bl.analyse_id,bl.executor_id) is null and bl.date_booking is null  and bl.equipment_id is not null then bl.equipment_id = v.equipment_id
                                when coalesce(bl.analyse_id,bl.equipment_id) is null and bl.date_booking is null  and bl.executor_id is not null then bl.executor_id = v.operator_id
                                when coalesce(bl.equipment_id,bl.executor_id) is null  then  bl.date_booking = date::DATE and  bl.analyse_id = z.analazy_id
                                when coalesce(bl.executor_id) is null  then  bl.date_booking = date::DATE and  bl.analyse_id = z.analazy_id and bl.equipment_id = v.equipment_id
                                else bl.date_booking = date::DATE and  bl.analyse_id = z.analazy_id and bl.equipment_id = v.equipment_id and bl.executor_id = v.operator_id
                            end 
                            left join used_limits_analese_equipment ul on ul.analyse_id = z.analazy_id and ul.equipment_id = v.equipment_id
                            left join executor_limit exl on exl.executor_id = v.operator_id
                            left join equipment_limit eql on eql.equipment_id = v.equipment_id
                            right join days_working dw on dw.d = EXTRACT(DOW from date::DATE)
                            right join days_employes de on de.d = EXTRACT(DOW from date::DATE) and de.executor_id = v.operator_id
                    where status = 'active' 
                        {blocking_element} and y.id = '{uuids_json['user_id']}'  
                        and bl.id is null
                        and {uuids_json['date_text']}
                        and {uuids_json['analyze_val']}
                        and {uuids_json['equipment_val']}
                        and {uuids_json['operator_val']}
                       """)
        availible_values = await db.execute(new_values_query)
        print(availible_values)
        list_availible_values = availible_values.fetchall()

        return list_availible_values

    @staticmethod
    async def get_period(
            db: AsyncSession,
            user: object,
            request_dict_prev: Dict
    ) -> None:
        responsible_person = await db.execute(text(
            f"SELECT responsible_person,project_name, is_priority  FROM \"project\" WHERE project_nick = '{user.username}' LIMIT 1;"))
        items = responsible_person.fetchall()

        today = datetime.today()
        date_str = today.strftime('%d.%m.%Y')
        time_str = today.strftime('%H:%M')
        is_open_global = await db.execute(text(
            f"""SELECT week_period  FROM \"control_enter_openwindowforordering\" 
                        WHERE start_date = '{date_str}'
                        and CAST('{time_str}' AS time) between CAST(start_time AS time) and CAST(end_time AS time) and for_priority = {items[0][2]}
                        ;"""))
        is_open_items = is_open_global.fetchall()
        print('is_open_items')
        print(is_open_items)
        if not is_open_items:
            is_open_local = await db.execute(text(
                f"""SELECT week_period  FROM \"control_enter_isopenregistration\" 
                                    WHERE is_open = True
                                    ;"""))
            is_open_l_items = is_open_local.fetchall()
            print(is_open_l_items)
        else:
            is_open_l_items = None
        if is_open_l_items and is_open_items :
            raise HTTPException(status_code=403,
                                detail="Создание записи запрещено администратором.")
        else:
            choose_not_null = is_open_l_items[0][0] if not is_open_items else is_open_items[0][0]
            start_date, end_date = choose_not_null.split('-')
            # Формируем словарь с ключами 'start' и 'end'
            request_dict_prev['start'] =  start_date.strip()
            request_dict_prev['end'] = end_date.strip()
            # Преобразуем словарь в JSON-строку
            return request_dict_prev

    @staticmethod
    async def get_possible_create_booking(
            request_data: PossibleCreateBookingRequest,
            response,
            db: AsyncSession,
            user: object,
            cookie_createkey: Optional[str] = None
    ) -> PossibleCreateBookingResponse:

        if user.is_superuser:
            raise HTTPException(status_code=403, detail="Создание записи администратором запрещено")
        request_dict_prev = request_data.dict(exclude_unset=True)

        request_dict = await UserBookingService.get_period(
            db,user,
            request_dict_prev)
        date_booking_dict = await UserBookingService.validate_date_booking(request_dict)
        print('date_booking_dict')
        uuids_json = await UserBookingService.get_uuids(db,user.username, request_dict)
        if not cookie_createkey and set(request_dict.keys()) == {"start","end"}:
            # Если токен отсутствует, создаем новый
            cookie_createkey = await UserBookingService.create_new_cookie_key(db,
                                                                          uuids_json['user_id'])
            response.set_cookie(key="createkey", value=cookie_createkey)

        if cookie_createkey and set(request_dict.keys()) == {"start","end"}:
            # Блокируем старый токен
            await UserBookingService.block_cookie_key(db,
                                                  cookie_createkey)
            # Если токен отсутствует, создаем новый
            cookie_createkey = await UserBookingService.create_new_cookie_key(db,
                                                                          uuids_json['user_id'])
            response.set_cookie(key="createkey", value=cookie_createkey)

        # Если токен передан, проверяем его срок действия
        elif cookie_createkey:
            await UserBookingService.validate_token(db, cookie_createkey)
        else:
            raise HTTPException(status_code=403, detail="Заполнение запрещено")

        await UserBookingService.update_blocking_period(db, uuids_json, cookie_createkey)

        list_availible_values = await UserBookingService.availible_values(db,
                                            uuids_json,
                                            date_booking_dict,
                                            ''
                                            )

        print(list_availible_values)

        if not list_availible_values:
            raise HTTPException(status_code=404,
                                detail="Нет доступных вариантов")

        date_json = {}
        analyze_json = {}
        equipment_json = {}
        executor_json = {}
        samples_list = []
        samples_used = []
        for val in list_availible_values:

            const_date = val[0].strftime('%d.%m.%Y')

            for elem in date_booking_dict['dates_list']:
                if elem in date_json and  elem == const_date:
                    date_json[elem] = True
                elif elem in date_json :
                    date_json[elem] = date_json[elem]
                else:
                    date_json[elem] = (elem == const_date)
            analyze_json[val[12]] = str(val[3])
            equipment_json[val[13]] = str(val[4])
            executor_json[val[14]] = str(val[6])

            samples_list.append(val[7])
            samples_used.append(val[9])

        print(uuids_json)
        const_samples_limit = int(list(set(samples_list))[0])
        const_samples_used = int(list(set(samples_used))[0])

        return PossibleCreateBookingResponse(
            date=date_json,
            analyse=analyze_json,
            equipment=equipment_json,
            executor=executor_json,
            samples_limit=const_samples_limit,
            used=const_samples_used
        )

    @staticmethod
    async def checking_blocking_period_with_creating(db: AsyncSession,
                                     uuids_json,
                                     cookie_createkey) -> None:
        check_query = text(f"""
                    SELECT cookies_key is null
                    FROM public.block_booking
                    WHERE cookies_key = '{cookie_createkey}' 
                        and date_booking = '{uuids_json['date_val']}'::date
                        and analyse_id = {uuids_json['analyze_id']}
                        and equipment_id = {uuids_json['equipment_id']}
                        and executor_id =  {uuids_json['operator_id']}
                    LIMIT 1
                """)
        result = await db.execute(check_query)
        row = result.fetchone()
        if row[0]:
            raise HTTPException(status_code=404,
                                detail="Проверка не пройдена")


    @staticmethod
    async def create_booking(
            request_data,
            response,
            db: AsyncSession,
            user: object,
            cookie_createkey: Optional[str] = None
    ) -> int:

        request_dict = request_data.dict(exclude_unset=True)
        print('request_dict')
        print(request_dict)
        if not cookie_createkey:
            raise HTTPException(status_code=403, detail="Запись запрещена")

        await UserBookingService.validate_token(db, cookie_createkey)

        print(user)
        uuids_json = await UserBookingService.get_uuids(db, user.username,
                                                    request_dict)

        await UserBookingService.checking_blocking_period_with_creating(db, uuids_json,
                                           cookie_createkey)

        print(request_dict)
        print(uuids_json)
        insert_query = text(f"""
                INSERT INTO public.projects_booking
                (project_id, date_booking, analyse_id, equipment_id, executor_id, count_analyses, status,is_delete,comment)
                VALUES ('{uuids_json['user_id']}', '{uuids_json['date_val']}',{uuids_json['analyze_id']}, {uuids_json['equipment_id']}
                , {uuids_json['operator_id']}, '{request_dict['samples']}', '{'На рассмотрении'}',False,'')
                RETURNING id
            """)

        try:
            result = await db.execute(insert_query)
            # Получаем идентификатор новой записи
            new_id = result.scalar()
            await UserBookingService.block_cookie_key(db,
                                                      cookie_createkey)
            await db.commit()
            return new_id
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500,
                                detail=f"Ошибка при добавлении записи: {e}")

    @staticmethod
    async def booking_info(db: AsyncSession, row):
        (project_id, date_booking, analyse_id, equipment_id
         , executor_id, count_analyses, status, comment) = row
        try:
            project_query = await db.execute(text(
                f"SELECT project_name FROM \"project\" WHERE id = '{project_id}' ;"))
            project_name = str(project_query.scalars().all()[0])
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Неверный формат проекта: {e}")

        try:
            date_info = date_booking.strftime('%d.%m.%Y')
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Неверный формат даты: {e}")

        try:
            analyze_query = await db.execute(text(
                f"SELECT analyze_name FROM \"analyze\" WHERE id = '{analyse_id}' ;"))
            analyze_name = str(analyze_query.scalars().all()[0])
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Неверный формат анализа: {e}")

        try:
            equipment_query = await db.execute(text(
                f"SELECT name FROM \"equipment\" WHERE id = '{equipment_id}' ;"))
            equipment_name = str(equipment_query.scalars().all()[0])
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Неверный формат оборудования: {e}")

        try:
            executor_query = await db.execute(text(
                f"SELECT  concat(first_name,' ',last_name,' ',patronymic)  FROM \"executor\" WHERE id = '{executor_id}' ;"))
            executor_fio = str(executor_query.scalars().all()[0])
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Неверный формат исполнителя: {e}")


        info_json = {
            'project_id': project_id,
            'project_name': project_name,
            'date_info': date_info,
            'analyze_name': analyze_name,
            'equipment_name': equipment_name,
            'executor_fio': executor_fio,
            'count_analyses': count_analyses,
            'status': status,
            'comment': comment
        }

        return info_json

    @staticmethod
    async def get_possible_changes(request_data,
                                   user,
                                   db: AsyncSession) -> PossibleChangesResponse:
        if not user.is_staff:
            raise HTTPException(status_code=403, detail="Изменение записи пользователем запрещено")
        request_dict = request_data.dict(exclude_unset=True)

        # request_dict = await UserBookingService.get_period(
        #     db, user)
        #


        # Пример запроса для получения данных по заявке (адаптируйте по вашей схеме)
        query = text("""
               SELECT project_id, date_booking, analyse_id, equipment_id, executor_id, count_analyses, status, comment
               FROM projects_booking
               WHERE id = :booking_id and is_delete = False  and status not in  ('Оценить')
               LIMIT 1
           """)

        result = await db.execute(query, {
            "booking_id": request_dict['id']
            # "date_start" : date_booking_dict['date_start'],
            # "date_end": date_booking_dict['date_end']
        })
        row = result.fetchone()
        print(row)
        if not row:
            raise HTTPException(status_code=404, detail="Запись не найдена")

        booking_info = await UserBookingService.booking_info(db,row)

        print(booking_info)
        # Распаковываем полученные данные
        project_id, date_booking, analyse_id, equipment_id, executor_id, count_analyses, status, comment = row

        request_dict['certian_date'] = date_booking

        date_booking_dict = await UserBookingService.validate_date_booking(
            request_dict)

        request_dict['date_booking'] = date_booking.strftime('%d.%m.%Y')
        request_dict['analyze_id'] = analyse_id

        uuids_json = await UserBookingService.get_uuids(db, user.username,
                                                        request_dict)
        print(date_booking_dict)
        print('uuids_json')
        list_availible_values = await UserBookingService.availible_values(db,
                                                                          uuids_json,
                                                                          date_booking_dict,
                                                                          '-----'
                                                                          )
        print(list_availible_values)
        if not list_availible_values:
            raise HTTPException(status_code=404,
                                detail="Нет доступных вариантов")

            # Преобразуем результаты в списки для формирования ответа
        projects_json = {}
        date_json = {}
        analyze_json = {}
        equipment_json = {}
        executor_json = {}
        samples_list = []
        samples_used = []

        for val in list_availible_values:

            const_date = val[0].strftime('%d.%m.%Y')

            for elem in date_booking_dict['dates_list']:
                if elem in date_json and  elem == const_date:
                    date_json[elem] = True
                elif elem in date_json:
                    date_json[elem] = date_json[elem]
                else:
                    date_json[elem] = (elem == const_date)
            analyze_json[val[12]] = str(val[3])
            equipment_json[val[13]] = str(val[4])
            executor_json[val[14]] = str(val[6])

            samples_list.append(val[7])
            samples_used.append(val[9])

        print(samples_list)
        const_samples_limit = int(list(set(samples_list))[0])
        const_samples_used = int(list(set(samples_used))[0])

        print(booking_info)
        return PossibleChangesResponse(
                chose=ChoseData(
                    project=booking_info['project_name'],
                    date=booking_info['date_info'],
                    analyse=booking_info['analyze_name'],
                    equipment=booking_info['equipment_name'],
                    executor=booking_info['executor_fio'],
                    samples=booking_info['count_analyses'],
                    status=booking_info['status'],
                    comment=booking_info['comment'] or ''
                ),
                change=ChangeData(
                    date=date_json,
                    analyse=analyze_json,
                    equipment=equipment_json,
                    executor=executor_json,
                    samples_limit=const_samples_limit,
                    samples_used = const_samples_used,
                    status={
                                # '0': 'Не выбран',
                                "start": 'На рассмотрении',
                                "get": 'Принято',
                                "rejected": 'Отклонено',
                                # "checked": 'Оценить',
                                # "done": 'Выполнено',
                            }
                )
            )

    @staticmethod
    async def change_booking(
            request_data: ChangeRequest,
            user,
            db: AsyncSession,
    ) -> ChangeResponse:
        """
        Изменяет запись в таблице projects_booking на основе входных данных.

        Шаги:
         1. Парсит дату из строки.
         2. Получает текущую запись по request_data.id.
         3. Получает новые идентификаторы для полей project, analyze, equipment, executor.
         4. Сравнивает текущие и новые значения и формирует словарь изменений.
         5. Если изменений нет, возвращает ответ с пустым словарем changed_fields.
         6. Иначе, обновляет запись и возвращает id и словарь изменённых полей.
        """
        if not user.is_staff:
            raise HTTPException(status_code=403, detail="Изменение записи пользователем запрещено")
        request_dict = request_data.dict(exclude_unset=True)

        date_booking_dict = await UserBookingService.validate_date_booking(
            request_dict)

        print(date_booking_dict)

        # Пример запроса для получения данных по заявке (адаптируйте по вашей схеме)
        query = text("""
                       SELECT project_id, date_booking, analyse_id, equipment_id, executor_id, count_analyses, status, comment
                       FROM projects_booking
                       WHERE id = :booking_id and is_delete = False and date_booking between :date_start and :date_end
                       LIMIT 1
                   """)

        result = await db.execute(query, {
            "booking_id": request_dict['id'],
            "date_start": date_booking_dict['date_start'],
            "date_end": date_booking_dict['date_end']
        })
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Запись не найдена")

        booking_info = await UserBookingService.booking_info(db, row)

        uuids_json = await UserBookingService.get_uuids(db, user.username,
                                                         request_dict)


        # 4. Сравнение текущих и новых значений
        changes: Dict[str, Dict[str, Any]] = {}
        if str(booking_info.get("project_name")) != request_dict["project"]:
            changes["project"] = {"old": str(booking_info.get("project_name")),
                                     "new": request_dict["project"]}
        if booking_info.get("date_info") != request_dict['date']:
            changes["date_booking"] = {
                "old": booking_info.get("date_info"),
                "new": request_dict['date']}
        if str(booking_info.get("analyze_name")) != request_dict["analyse"]:
            changes["analyze"] = {"old": str(booking_info.get("analyze_name")),
                                     "new": request_dict["analyse"]}
        if str(booking_info.get("equipment_name")) != request_dict["equipment"]:
            changes["equipment"] = {
                "old": str(booking_info.get("equipment_name")),
                "new": request_dict["equipment"]}
        if str(booking_info.get("executor_fio")) != request_dict["executor"]:
            changes["executor"] = {
                "old": str(booking_info.get("executor_fio")),
                "new": request_dict["equipment"]}
        if booking_info.get("count_analyses") != request_dict["samples"]:
            changes["samples"] = {
                "old": booking_info.get("count_analyses"), "new": request_dict["samples"]}
        if booking_info.get("status") != request_dict["status"]:
            changes["status"] = {"old": booking_info.get("status"),
                                 "new": request_dict["status"]}
        if booking_info.get("comment") != request_dict["comment"]:
            changes["comment"] = {"old": booking_info.get("comment"),
                                  "new": request_dict["comment"]}

        print(changes)
        print('----')
        print(uuids_json)
        #5. Если изменений нет, возвращаем сообщение с пустым changed_fields
        if not changes:
            return ChangeResponse(id=request_dict['id'], changed_fields={})

        # 6. Обновление записи
        update_query = text(f"""
               UPDATE public.projects_booking
               SET project_id = '{booking_info["project_id"]}',
                   date_booking = '{datetime.strptime(request_dict['date'],
                                              '%d.%m.%Y').date()}',
                   analyse_id = {uuids_json["analyze_id"]},
                   equipment_id = {uuids_json["equipment_id"]},
                   executor_id = {uuids_json["operator_id"]},
                   count_analyses = {request_dict["samples"]},
                   is_delete = False,
                   status = '{request_dict["status"]}',
                   comment = '{request_dict["comment"]}'
               WHERE id = {request_dict['id']}
               RETURNING id;
           """)
        try:
            update_result = await db.execute(update_query)
            updated_id = update_result.fetchone()[0]
            if updated_id is None:
                raise HTTPException(status_code=404,
                                    detail="Запись не найдена или не обновлена")
            await db.commit()
            return ChangeResponse(id=updated_id, changed_fields=changes)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500,
                                detail=f"Ошибка при обновлении записи: {e}")

    @staticmethod
    async def cancel_booking(
            request_data: CancelRequest,
            user,
            db: AsyncSession,
    ) -> ChangeResponse:

        request_dict = request_data.dict(exclude_unset=True)

        # date_booking_dict = await UserBookingService.validate_date_booking(
        #     request_dict)


        block_query = '-----' if user.is_staff  else ''
        query = text(f"""
                               SELECT x.project_id, x.date_booking, x.analyse_id, x.equipment_id, x.executor_id, x.count_analyses, x.status, x.comment
                               FROM projects_booking x
                               join project p on p.id = x.project_id
                               WHERE x.id = '{request_dict['id']}' and x.is_delete = False 
                               and :date_end
                               {block_query} and p.project_nick = '{user.username}'
                               LIMIT 1
                           """)

        result = await db.execute(query)
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Запись не найдена")

        (project_id, date_booking, analyse_id, equipment_id
         , executor_id, count_analyses, status, comment) = row

        if not user.is_staff and status != 'На рассмотрении':
            raise HTTPException(status_code=403, detail="Удаление запрещено")

        else:
            update_query = text(f"""
                           UPDATE public.projects_booking
                           SET is_delete = True
                           WHERE id = {request_dict['id']}
                           RETURNING id;
                       """)
            try:
                delete_result = await db.execute(update_query)
                deleted_id = delete_result.fetchone()[0]
                if not deleted_id:
                    raise HTTPException(status_code=404,
                                        detail="Запись не найдена или не обновлена")
                await db.commit()
                return CancelResponse(id=deleted_id, data="Запись успешно удалена")
            except Exception as e:
                await db.rollback()
                raise HTTPException(status_code=500,
                                    detail=f"Ошибка при обновлении записи: {e}")

    @staticmethod
    async def feedback_booking(
            request_data: FeedbackRequest,
            user,
            db: AsyncSession,
    ) -> FeedbackResponse:
        pass