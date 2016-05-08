title: Solr权限控制
tags:
  - security
  - solr
id: 994
categories:
  - 搜索引擎
date: 2015-01-20 21:47:37
---

有些情况下，想给Solr增加权限控制，这样就不会被随意更新和删除。关于这点，在[https://wiki.apache.org/solr/SolrSecurity](https://wiki.apache.org/solr/SolrSecurity)有详细的描述。觉得最坑人的一点是Solr-4470还没resolved。不管它，先使用Jetty添加权限控制

下载已经编译好的solr-4.8.0,进入example目录
编辑etc/webdefault.xml,添加如下内容:
```
<security-constraint>
    <web-resource-collection>
      <web-resource-name>Solr authenticated application</web-resource-name>
      <url-pattern>/update/*</url-pattern>
    </web-resource-collection>
    <auth-constraint>
      <role-name>update-role</role-name>
    </auth-constraint>
  </security-constraint>

  <login-config>
    <auth-method>BASIC</auth-method>
    <realm-name>Solr Update</realm-name>
  </login-config>

```
编辑 etc/jetty.xml, 添加如下内容：
```
<Call name="addBean">
  <Arg>
    <New class="org.eclipse.jetty.security.HashLoginService">
      <Set name="name">Solr Update</Set>
      <Set name="config"><SystemProperty name="jetty.home" default="."/>/etc/realm.properties</Set>
      <Set name="refreshInterval">0</Set>
    </New>
  </Arg>
</Call>
```
增加 etc/realm.properties,写入如下内容，也就是用户名，密码以及角色：
```
index: update, update-role
```
启动solr,到exampledocs目录下执行./post.sh solr.xml,返回401错误，说明未认证。修改post.sh,在调用curl时加上用户名和密码，如下：
curl --user index:update $URL --data-binary @$f -H 'Content-type:application/xml'

再次执行./post.sh solr.xml,执行成功，到solr后台查看,可以看到添加文件成功,说明认证设置成功
