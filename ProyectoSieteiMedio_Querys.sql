-- Query Nº1
select username,descripcion,carta_inicial from
(select a.id_participante,username,descripcion,max(a.cnt) contador
from (select p.id_participante,u.username,b.descripcion,count(t.carta_inicial) cnt 
from turnos t
inner join participante p on p.id_participante=t.idparticipante
inner join jugador j on j.idjugador=p.id_jugador
left join usuario u on u.idusuario=j.idusuario
left join bot b on b.idbot=j.idbot
group by u.username,b.descripcion,t.carta_inicial
) a
group by username,descripcion) c
inner join
(select idparticipante, carta_inicial,count(carta_inicial) contador2 from turnos group by carta_inicial,idparticipante) d
on c.id_participante = d.idparticipante
where contador = contador2
group by username,descripcion;

-- Query Nº2
select username,descripcion from(
select u.username,descripcion,max(t.apuesta)puntos,t.idpartida,t.idparticipante
from turnos t
inner join participante p on p.id_participante=t.idparticipante
inner join jugador j on j.idjugador=p.id_jugador
left join usuario u on u.idusuario=j.idusuario
left join bot b on b.idbot = j.idbot
group by idpartida,idparticipante
order by idpartida) as a
inner join
(select max(apuesta) puntos2,idpartida,idparticipante
from turnos
group by idpartida) as c
where a.puntos=c.puntos2 and a.idpartida=c.idpartida
group by a.idparticipante,a.idpartida;

-- Query Nº3
select username,descripcion from(
select u.username,descripcion,min(t.apuesta)puntos,t.idpartida,t.idparticipante
from turnos t
inner join participante p on p.id_participante=t.idparticipante
inner join jugador j on j.idjugador=p.id_jugador
left join usuario u on u.idusuario=j.idusuario
left join bot b on b.idbot = j.idbot
group by idpartida,idparticipante
order by idpartida) as a
inner join
(select min(apuesta) puntos2,idpartida,idparticipante
from turnos
group by idpartida) as c
where a.puntos=c.puntos2 and a.idpartida=c.idpartida
group by a.idpartida;

-- Query Nº5
select *
from ( select round(count(ganador_partida)*100/count(idpartida)) as "Porcentaje %" from partida p
inner join participante pa on p.ganador_partida=pa.id_participante
inner join jugador j on pa.id_jugador=j.idjugador
inner join bot b on j.idbot=b.idbot
where ganador_partida=pa.id_participante) as contador;

-- Query Nº7
select idpartida,count(numero_turno) as "Rondas Ganadas",descripcion Palo from turnos t
left join cartas c
on t.carta_inicial = c.idcartas
left join tipo_carta tc
on c.tipo = tc.idtipo_carta 
where puntos_final > puntos_inicio
group by idpartida,Palo;

-- Query Nº8
select idpartida,count(numero_turno) as "Rondas Ganadas" from turnos t
left join cartas c
on t.carta_inicial = c.idcartas
left join tipo_carta tc
on c.tipo = tc.idtipo_carta 
where puntos_final > puntos_inicio and es_banca = 1
group by idpartida;

-- Query Nº9
select count(es_banca), idpartida
from turnos
where es_banca=1
group by idpartida;

-- Query Nº10
select par.idpartida,t.idparticipante,u.username,b.descripcion,par.nombre_sala,max(t.puntos_final),if(par.ganador_partida=t.idparticipante,"Si","No") as ganador
from partida par
inner join turnos t on t.idpartida=par.idpartida
inner join participante p on p.id_participante=t.idparticipante
inner join jugador j on j.idjugador=p.id_jugador
left join usuario u on u.idusuario=j.idusuario
left join bot b on b.idbot=j.idbot
where par.idpartida IN (select idparticipante
from turnos
group by idparticipante)
 and t.puntos_final IN 
(select max(puntos_final)
from turnos
group by idparticipante)
group by u.username,b.descripcion;

select * from turnos;
-- Query Nº11
select avg(apuesta), idpartida
from turnos
group by idpartida;

-- Query Nº13
select sum(truncate(c.valor,1)) as "Valor por partida", count(t.carta_inicial) as "Cantidad"
from cartas c
inner join turnos t on c.idcartas=t.carta_inicial
group by t.idpartida;

-- Query Nº14
select t5.p2-t1.p1 diferencia from
(select distinct puntos_inicio p1
from turnos t
where numero_turno = 1
group by idpartida) t1,
(
select puntos_inicio p2
from turnos
where numero_turno = 5) t5;
