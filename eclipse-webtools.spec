%{?scl:%scl_package eclipse-webtools}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 3

%global qualifier             v$(date -u +%G%m%d%H00)

%bcond_with datatools

Name:           %{?scl_prefix}eclipse-webtools
Version:        3.8.0
Release:        1.%{baserelease}%{?dist}
Summary:        Eclipse Webtools Projects

License:        EPL
URL:            http://www.eclipse.org/webtools/
BuildArch:      noarch

# git clone --recursive git://git.eclipse.org/gitroot/webtools/webtools.releng.aggregator.git
# pushd webtools.releng.aggregator
# sh ./scripts/submodule-checkout.sh 
# popd
# find webtools.releng.aggregator/ -name *.jar -type f -delete
# find webtools.releng.aggregator/ -name *.class -type f -delete
# find webtools.releng.aggregator/ -name *.zip -type f -delete
# rm -rf webtools.releng.aggregator/webtools.releng/releng.wtptools/api/org.eclipse.wtp.releng.wtpbuilder/
# mkdir eclipse-webtools-3.8.0/ && pushd webtools.releng.aggregator
# cp -R pom.xml webtools.* wtp-parent/ ../eclipse-webtools-3.8.0/ && popd
# tar cfJv eclipse-webtools-3.8.0.tar.xz eclipse-webtools-3.8.0/
Source0:        %{pkg_name}-%{version}.tar.xz

# Missing plugin (maybe this should be provided by eclipselink package in future)
Source1:        http://git.eclipse.org/c/eclipselink/eclipselink.runtime.git/snapshot/eclipselink.runtime-7816e2b523adf5e65ad0c245f13ca4b59ff329f2.tar.bz2

# Remove org.mozilla.javascript bundle from jsdt feature
Patch0:         %{pkg_name}-rm-moz-js-from-jsdt-feature.patch

# Remove org.mozilla.javascript.source bundle from jsdt source feature
Patch1:         %{pkg_name}-rm-moz-js-src-from-jsdt-src-feature.patch

# Remove bundles org.eclipse.persistence.moxy and
# org.eclipse.jpt.jaxb.eclipselink.core.schemagen from
# webtools.dali/jaxb/features/org.eclipse.jpt.jaxb.eclipselink.feature/feature.xml
Patch2:         %{pkg_name}-rm-unavailable-plugins-from-jaxb-eclipselink-feature.patch

# Dont limit version of javax.wsdl in
# webtools.webservices/features/org.eclipse.wst.ws_wsdl15.feature/feature.xml
Patch3:         %{pkg_name}-rm-javax.wsdl-version-check-from-wsdl15-feature.patch

# Remove version checks from
# webtools.sourceediting/features/org.eclipse.wst.xml_core.feature/feature.xml
Patch4:         %{pkg_name}-rm-version-checks-from-xml_core-feature.patch

# Remove version checks of org.jdom, javax.wsdl, and
# disable javax.jws, javax.xml.stream and javax.xml.ws from
# webtools.webservices.jaxws/features/org.eclipse.jst.ws.cxf.feature/feature.xml
Patch5:         %{pkg_name}-rm-version-checks-and-obstacle-bundles-from-jst.ws.cxf-feature.patch

# Remove version checks of org.apache.commons.logging, javax.xml.soap from
# webtools.webservices/features/org.eclipse.wst.ws_core.feature/feature.xml
Patch6:         %{pkg_name}-wst.ws_core.feature.patch

# Disable org.apache.commons.logging, org.apache.bcel, java_cup.runtime from
# webtools.sourceediting.xsl/features/org.eclipse.wst.xsl.feature/feature.xml
Patch7:         %{pkg_name}-wst.xsl.feature.patch 

# Fix xerces api change (a method needs to return a String)
Patch8:         %{pkg_name}-xerces-api-change.patch

# Add unimplemented methods for javax.wsdl
# Upstream bug: https://bugs.eclipse.org/bugs/show_bug.cgi?id=265772
Patch9:         0001-Implement-missing-methods-needed-for-WSDL4J-1.6.2.patch

# fix to work with fedora packaged xerces-j2 (more up-to-date)
Patch10:         %{pkg_name}-xerces-j2-api-change.patch

# Remove version check for javax.persistence
Patch13:        %{pkg_name}-javax.persistence-version.patch

# Remove more version checks
Patch14:        %{pkg_name}-rm-version-checks-from-jst.ws.jaxws-feature.patch
Patch15:        fix-cxf.creation.core.patch
Patch16:        fix-comparator.patch
Patch17:        rm-gson-from-nodejs-feature.patch
Patch18:        rm-jetty-from-wst-server-feature.patch

# Accomodate for older jetty
Patch19:        old-jetty.patch

# Fix break points intefering with CDT
Patch20:        breakpoint_interference.patch

BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix}tycho
BuildRequires:  %{?scl_prefix}tycho-extras
%if %{with datatools}
BuildRequires:  eclipse-dtp
%endif
BuildRequires:  %{?scl_prefix}eclipse-emf-runtime
BuildRequires:  %{?scl_prefix}eclipse-gef >= 3.11.0
BuildRequires:  %{?scl_prefix}eclipse-jdt
BuildRequires:  %{?scl_prefix}eclipse-license
BuildRequires:  %{?scl_prefix}eclipse-pde
BuildRequires:  %{?scl_prefix}eclipse-xsd
BuildRequires:  %{?scl_prefix}osgi(javax.servlet-api)
BuildRequires:  %{?scl_prefix}osgi(javax.wsdl)
BuildRequires:  %{?scl_prefix_java_common}osgi(javax.xml.bind)
BuildRequires:  %{?scl_prefix_java_common}osgi(java_cup.runtime)
BuildRequires:  %{?scl_prefix}osgi(org.apache.axis)
BuildRequires:  %{?scl_prefix}osgi(org.apache.wsil4j)
BuildRequires:  %{?scl_prefix_java_common}osgi(org.eclipse.jetty.http)
BuildRequires:  %{?scl_prefix_java_common}osgi(org.eclipse.jetty.webapp)
BuildRequires:  %{?scl_prefix_java_common}osgi(org.jdom)
BuildRequires:  %{?scl_prefix}osgi(org.uddi4j)

%description
Eclipse Webtools. This contains sub-packages for different sub-projects
of Eclipse Webtools project, including Server Tools, SourceEditing Tools,
Webservices Tools, Java EE Tools, JSF Tools, and Dali (JPA) Tools. 

%package        common
Summary:        WST Common UI and Faceted Project Framework
Requires:       %{?scl_prefix}eclipse-gef >= 3.11.0
# Obsoletes/Provides added in F24
Provides:       %{name}-common-core = %{version}-%{release}
Provides:       %{name}-servertools-core = %{version}-%{release}
Obsoletes:      %{name}-common-core < 3.8.0-1
Obsoletes:      %{name}-servertools-core < 3.8.0-1

%description common
This package includes WST common UI functionality, and faceted projects
framework. The Faceted Project Framework allows the plugin developer to think
of projects as composed of units of functionality, otherwise known as facets,
that can be added and removed by the user.

%package        servertools
Summary:        Eclipse Server Tools Framework

%description servertools
This package includes Server tools framework UI, and adapters for use
with the WST and JST server tools.

%package        sourceediting
Summary:        Eclipse Web Developer, XML, XPath, and XSL Tools

%description sourceediting
Eclipse Web Developer Tools, including HTML, CSS, XHTML, etc.

XML, DTD and XML Schema Editors, validators, and XML Catalog support

PscyhoPath XPath 2.0 Processor Feature

XSLT Editor, validator, launching and debugging support

JavaScript Development Tools

%package        javaee
Summary:        Eclipse Java EE Developer Tools
# Obsoletes/Provides added in F24
Provides:       %{name}-webservices = %{version}-%{release}
Obsoletes:      %{name}-webservices < 3.8.0-1

%description javaee
Eclipse Java EE Developer Tools including APIs and models for working
with JavaServer Pages (JSP) and the creation of Dynamic Web Projects,
the Web Services Explorer, WSDL Editor, WS-I Validator, Service
Policy Preferences, and more.

%package        jsf
Summary:        Eclipse Web Tools Platform JavaServer Faces (JSF) Tools

%description jsf
Eclipse Web Tools Platform JavaServer Faces Tools, including
Web Page Editor and Tag Library Metadata (Apache Trinidad).

%if %{with datatools}
%package        dali
Summary:        Eclipse Dali Java Persistence (JPA) Tools

%description dali
Dali Java Persistence Tools with JPA and JAXB Support.
%endif

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -n %{pkg_name}-%{version} -q

tar xfj %{SOURCE1}
pushd eclipselink.runtime-7816e2b523adf5e65ad0c245f13ca4b59ff329f2/
cp -r jpa/org.eclipse.persistence.jpa.jpql/ ../webtools.dali/jpa/plugins/
popd
rm -r eclipselink.runtime-7816e2b523adf5e65ad0c245f13ca4b59ff329f2/

# Find and delete any hidden jar or zip files
find -name *.class -type f -delete
find -name *.jar ! -name json_simple* -type f -delete
find -name *.zip -type f -delete

# Configure org.eclipse.persistence.jpa.jpql to be built as part of this build
%pom_xpath_inject pom:project/pom:modules \
    "<module>jpa/plugins/org.eclipse.persistence.jpa.jpql</module>" webtools.dali
%pom_set_parent org.eclipse.webtools.dali:org.eclipse.webtools.dali:3.4.0-SNAPSHOT \
    webtools.dali/jpa/plugins/org.eclipse.persistence.jpa.jpql
%pom_xpath_inject pom:project/pom:parent "<relativePath>../../../</relativePath>" \
    webtools.dali/jpa/plugins/org.eclipse.persistence.jpa.jpql

# Jetty API change
sed -i -e "s/MimeTypes.TEXT_HTML/MimeTypes.Type.TEXT_HTML.toString()/" \
    webtools.servertools/plugins/org.eclipse.wst.server.preview/src/org/eclipse/wst/server/preview/internal/WTPDefaultHandler.java

# Build useless jar that is needed to build but does nothing
# See http://dev.eclipse.org/mhonarc/lists/wtp-dev/msg08607.html
# and PERFMSR.README.txt in org.eclipse.perfmsr.core.stub/
if [[ -e %{_prefix}/lib64/eclipse ]]; then
    CORE_RUNTIME_JAR=$(ls %{_prefix}/lib64/eclipse/plugins/org.eclipse.core.runtime_*)
else
    CORE_RUNTIME_JAR=$(ls %{_prefix}/lib/eclipse/plugins/org.eclipse.core.runtime_*)
fi
pushd webtools.common/plugins/org.eclipse.jem.util/org.eclipse.perfmsr.core.stub/src
    javac -cp $(build-classpath felix/org.osgi.core):${CORE_RUNTIME_JAR} \
        org/eclipse/perfmsr/core/*.java
    jar cf ../perfmsr.jar org/
popd

# Fix OSGi headers in manifests
## Remove some version ranges
## Don't Require-Bundle stuff provided by JDK
find -name MANIFEST.MF \
    -exec sed -i \
        -e "s/\(javax.wsdl\);bundle-version=..[0-9\.]\+,[0-9\.]\+../\1/g" \
        -e "s/\(javax.xml.soap\);.*,/\1,/" \
        -e "s/javax.jws;.*//" \
        -e "s/javax.xml.ws.*;version=.*,\?//" \
        -e "s/javax.xml.bind.*,\?$//g" \
        -e "s/\(org.eclipse.jetty.*\);bundle-version=..[0-9\.]\+,[0-9\.]\+../\1/g" \
        -e "s/org.junit;.*,/org.junit,/g" \
    {} \;

# Fix some specifics that the above breaks
sed -i -e "s/\(org.eclipse.jdt.apt.core;.*\),/\1/" \
    webtools.webservices.jaxws/bundles/org.eclipse.jst.ws.cxf.creation.ui/META-INF/MANIFEST.MF
sed -i -e "s/\(org.eclipse.jdt.apt.core;.*\),/\1/" \
    webtools.webservices.jaxws/bundles/org.eclipse.jst.ws.cxf.creation.core/META-INF/MANIFEST.MF
sed -i -e "s/Import-Package:\s*$//" \
    webtools.dali/jaxb/plugins/org.eclipse.jpt.jaxb.core.schemagen/META-INF/MANIFEST.MF
find -name MANIFEST.MF -exec sed -i -e "/^$/d" {} \;

# Make sure that axis-ant is required also. This is needed because of the not nice way
# that Eclipse consumes Axis, from that strange wrapper bundle in "Orbit" repository.
sed -i -e "s/org.apache.axis/org.apache.axis.tools,org.apache.axis/g" \
    webtools.webservices/bundles/org.eclipse.jst.ws.axis.consumption.core/META-INF/MANIFEST.MF

# Remove unavailable optional bundle from manifest because this bundle is
# shipped with "eclipse-tests" and not actually installed into the platform
sed -i -e "s/^.*update.core.*$//" -e "/^$/d" \
    webtools.servertools/plugins/org.eclipse.wst.server.core/META-INF/MANIFEST.MF

# Disable the Dali diagram editor (requires graphiti)
%pom_disable_module jpa_diagram_editor/development/org.eclipse.jpt.jpadiagrameditor.repository webtools.dali
%pom_disable_module jpa_diagram_editor/features/org.eclipse.jpt.jpadiagrameditor.feature webtools.dali
%pom_disable_module jpa_diagram_editor/features/org.eclipse.jpt.jpadiagrameditor_sdk.feature webtools.dali
%pom_disable_module jpa_diagram_editor/plugins/org.eclipse.jpt.jpadiagrameditor.branding webtools.dali
%pom_disable_module jpa_diagram_editor/plugins/org.eclipse.jpt.jpadiagrameditor.doc.user webtools.dali
%pom_disable_module jpa_diagram_editor/plugins/org.eclipse.jpt.jpadiagrameditor.ui webtools.dali

# Disable bits that rely on datatools when not available
%if ! %{with datatools}
%pom_disable_module webtools.dali
%pom_disable_module plugins/org.eclipse.jst.j2ee.ejb.annotations.ui webtools.ejb
%pom_xpath_remove "plugin[@id='org.eclipse.jst.j2ee.ejb.annotations.ui']" \
  webtools.javaee/features/org.eclipse.jst.enterprise_ui.feature/feature.xml
%endif

# Disable capabilities because they hide stuff by default
%pom_disable_module plugins/org.eclipse.wtp.jee.capabilities webtools.javaee
%pom_disable_module org.eclipse.wtp.javascript.capabilities webtools.sourceediting/bundles
%pom_disable_module org.eclipse.wtp.web.capabilities webtools.sourceediting/bundles
%pom_disable_module org.eclipse.wtp.xml.capabilities webtools.sourceediting/bundles

# Disable building all tests for now
%pom_disable_module webtools.releng
%pom_disable_module webtools.common.tests
%pom_disable_module tests/org.eclipse.wst.common.project.facet.core.tests webtools.common.fproj
%pom_disable_module tests/org.eclipse.wst.common.project.facet.ui.tests webtools.common.fproj
%pom_disable_module org.eclipse.wst.common.snippets.tests webtools.common.snippets
%pom_disable_module webtools.repositories
%pom_disable_module webtools.javaee.tests
%pom_disable_module tests webtools.sourceediting
%pom_disable_module org.eclipse.wst.web_tests.feature webtools.sourceediting/features
%pom_disable_module org.eclipse.wst.xml_tests.feature webtools.sourceediting/features
%pom_disable_module org.eclipse.wst.json_tests.feature webtools.sourceediting/features
%pom_disable_module webtools.sourceediting.xsl.tests
%pom_disable_module webtools.sourceediting.xpath.tests
%pom_disable_module webtools.jsf.tests
%pom_disable_module webtools.servertools.tests
%pom_disable_module features/org.eclipse.jst.server_adapters.ext_tests.feature webtools.servertools
%pom_disable_module features/org.eclipse.jst.server_tests.feature webtools.servertools
%pom_disable_module features/org.eclipse.wst.server_tests.feature webtools.servertools
%pom_disable_module assembly/features/org.eclipse.jpt.assembly.feature webtools.dali
%pom_disable_module assembly/features/org.eclipse.jpt_sdk.assembly.feature webtools.dali
%pom_disable_module assembly/features/org.eclipse.jpt.tests.assembly.feature webtools.dali
%pom_disable_module common/features/org.eclipse.jpt.common.tests.feature webtools.dali
%pom_disable_module common/tests/org.eclipse.jpt.common.core.tests webtools.dali
%pom_disable_module common/tests/org.eclipse.jpt.common.utility.tests webtools.dali
%pom_disable_module jpa/features/org.eclipse.jpt.jpa.eclipselink.feature webtools.dali
%pom_disable_module jpa/features/org.eclipse.jpt.jpa.eclipselink_sdk.feature webtools.dali
%pom_disable_module jpa/features/org.eclipse.jpt.jpa.eclipselink.tests.feature webtools.dali
%pom_disable_module jpa/plugins/org.eclipse.jpt.jpa.eclipselink.core.ddlgen webtools.dali
%pom_disable_module jpa/features/org.eclipse.jpt.jpa.tests.feature webtools.dali
%pom_disable_module jpa/tests/org.eclipse.jpt.jpa.core.tests webtools.dali
%pom_disable_module jpa/tests/org.eclipse.jpt.jpa.core.tests.extension.resource webtools.dali
%pom_disable_module jpa/tests/org.eclipse.jpt.jpa.eclipselink.core.tests webtools.dali
%pom_disable_module jaxb/features/org.eclipse.jpt.dbws.eclipselink_sdk.feature webtools.dali
%pom_disable_module jaxb/features/org.eclipse.jpt.jaxb.eclipselink_sdk.feature webtools.dali
%pom_disable_module jaxb/features/org.eclipse.jpt.dbws.eclipselink.feature webtools.dali
%pom_disable_module jaxb/plugins/org.eclipse.jpt.dbws.eclipselink.branding webtools.dali
%pom_disable_module jaxb/plugins/org.eclipse.jpt.dbws.eclipselink.core.gen webtools.dali
%pom_disable_module jaxb/plugins/org.eclipse.jpt.dbws.eclipselink.ui webtools.dali
%pom_disable_module jaxb/plugins/org.eclipse.jpt.jaxb.eclipselink.core.schemagen webtools.dali
%pom_disable_module jaxb/tests/org.eclipse.jpt.jaxb.eclipselink.core.tests webtools.dali
%pom_disable_module jaxb/tests/org.eclipse.jpt.jaxb.core.tests webtools.dali
%pom_disable_module jaxb/features/org.eclipse.jpt.jaxb.eclipselink.tests.feature webtools.dali
%pom_disable_module jaxb/features/org.eclipse.jpt.jaxb.tests.feature webtools.dali
%pom_disable_module jpa_diagram_editor/features/org.eclipse.jpt.jpadiagrameditor.tests.feature webtools.dali
%pom_disable_module jpa_diagram_editor/tests/org.eclipse.jpt.jpadiagrameditor.ui.tests webtools.dali
%pom_disable_module tests webtools.jsdt
%pom_disable_module org.eclipse.wst.jsdt_tests.feature webtools.jsdt/features
%pom_disable_module org.eclipse.wst.jsdt.chromium_tests.feature webtools.jsdt/features
%pom_disable_module tests/org.eclipse.jst.ws.axis.consumption.core.tests webtools.webservices
%pom_disable_module tests/org.eclipse.jst.ws.tests webtools.webservices
%pom_disable_module tests/org.eclipse.jst.ws.tests.performance webtools.webservices
%pom_disable_module tests/org.eclipse.wst.wsdl.tests webtools.webservices
%pom_disable_module tests/org.eclipse.wst.wsdl.tests.ui webtools.webservices
%pom_disable_module tests/org.eclipse.wst.wsdl.ui.tests webtools.webservices
%pom_disable_module tests/org.eclipse.wst.wsdl.validation.tests webtools.webservices
%pom_disable_module tests/org.eclipse.wst.wsi.tests webtools.webservices
%pom_disable_module tests/org.eclipse.wst.ws.tests webtools.webservices
%pom_disable_module features/org.eclipse.wst.ws_tests.feature webtools.webservices
%pom_disable_module tests/org.eclipse.jst.ws.cxf.tests webtools.webservices.jaxws
%pom_disable_module tests/org.eclipse.jst.ws.jaxb.core.tests webtools.webservices.jaxws
%pom_disable_module tests/org.eclipse.jst.ws.jaxws.core.tests webtools.webservices.jaxws
%pom_disable_module tests/org.eclipse.jst.ws.jaxws.dom.integration.tests webtools.webservices.jaxws
%pom_disable_module tests/org.eclipse.jst.ws.jaxws.dom.runtime.tests webtools.webservices.jaxws
%pom_disable_module tests/org.eclipse.jst.ws.jaxws.dom.ui.tests webtools.webservices.jaxws
%pom_disable_module tests/org.eclipse.jst.ws.jaxws.testutils webtools.webservices.jaxws
%pom_disable_module tests/org.eclipse.jst.ws.jaxws.utils.tests webtools.webservices.jaxws
%pom_disable_module tests/org.jmock webtools.webservices.jaxws
%pom_disable_module features/org.eclipse.jst.ws.cxf_tests.feature webtools.webservices.jaxws
%pom_disable_module features/org.eclipse.jst.ws.jaxws.assembly_tests.feature webtools.webservices.jaxws
%pom_disable_module features/org.eclipse.jst.ws.jaxws.dom_tests.feature webtools.webservices.jaxws
%pom_disable_module features/org.eclipse.jst.ws.jaxws_tests.feature webtools.webservices.jaxws
%pom_disable_module tests/org.eclipse.jst.ejb.ui.tests webtools.ejb

# Remove additional dep on javax.jws
%pom_xpath_remove pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration \
    webtools.webservices.jaxws/bundles/org.eclipse.jst.ws.jaxws.core
%pom_xpath_remove pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration \
    webtools.webservices.jaxws/bundles/org.eclipse.jst.ws.jaxws.ui
%pom_xpath_remove pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration \
    webtools.webservices.jaxws/tests/org.eclipse.jst.ws.jaxws.core.tests

# XMvn can't handle 'jsr14' as a target and it's unnecessary
%pom_xpath_set "pom:plugin[pom:artifactId = 'tycho-compiler-plugin']/pom:configuration/pom:target" \
  "1.5" webtools.sourceediting.xpath/bundles/org.eclipse.wst.xml.xpath2.processor

# No source bundles for external units
%pom_xpath_inject "pom:plugin[pom:artifactId = 'tycho-source-feature-plugin']/pom:executions/pom:execution/pom:configuration/pom:excludes" \
    "<plugin id=\"org.jdom\"/><plugin id=\"javax.wsdl\"/>" webtools.webservices.jaxws/features/org.eclipse.jst.ws.cxf.feature
%pom_xpath_inject "pom:plugin[pom:artifactId = 'tycho-source-feature-plugin']/pom:executions/pom:execution/pom:configuration/pom:excludes" \
    "<plugin id=\"org.jdom\"/><plugin id=\"javax.wsdl\"/>" webtools.webservices.jaxws/features/org.eclipse.jst.ws.jaxws.feature

# Undo global replacement from earlier in prep, so upstream patch can be
# applied more completely
sed -i -e "s/javax.wsdl/javax.wsdl;bundle-version=\"[1.5.0,1.6.0)\"/" \
   webtools.webservices/bundles/org.eclipse.wst.wsdl/META-INF/MANIFEST.MF

%patch0 -p0 -b .orig
%patch1 -p0 -b .orig
%patch2 -p0 -b .orig
%patch3 -p0 -b .orig
%patch4 -p0 -b .orig
%patch5 -p0 -b .orig
%patch6 -p0 -b .orig
%patch7 -p0 -b .orig
%patch8 -p0 -b .orig
%patch9 -p0 -b .orig
%patch10 -p0 -b .orig
%patch13 -p0 -b .orig
%patch14 -p0 -b .orig
%patch15
%patch16
%patch17
%patch18
%patch19
pushd webtools.jsdt
%patch20 -p1
popd

# Use glassfish, not tomcat
sed -i -e 's/javax\.servlet/javax.servlet-api/' \
  webtools.servertools/plugins/org.eclipse.wst.server.preview/META-INF/MANIFEST.MF

# Remove log4j
%pom_xpath_remove "plugin[@id='org.apache.log4j']" \
  webtools.sourceediting.xsl/features/org.eclipse.wst.xsl.feature/feature.xml
%pom_xpath_remove "plugin[@id='org.apache.log4j']" \
  webtools.webservices/features/org.eclipse.wst.ws_core.feature/feature.xml
%pom_xpath_remove "plugin[@id='javax.mail']" \
  webtools.webservices/features/org.eclipse.wst.ws_core.feature/feature.xml
%pom_xpath_remove "plugin[@id='javax.activation']" \
  webtools.webservices/features/org.eclipse.wst.ws_core.feature/feature.xml

%pom_xpath_set pom:project/pom:build/pom:pluginManagement/pom:plugins/pom:plugin/pom:configuration/pom:sourceReferences/pom:generate "false" wtp-parent

# Don't install poms
%mvn_package "::pom::" __noinstall

# SDK bits
%mvn_package ":*sdk{,.feature,.documentation}" __noinstall
%mvn_package ":*{.api.doc,.doc.api,.doc.isv,.doc.dev}" __noinstall
%mvn_package ":::sources{,-feature}:" __noinstall

# Common features and plugins
%mvn_package "org.eclipse.webtools.common:" common
%mvn_package ":org.eclipse.jst.common.frameworks" common
%mvn_package ":org.eclipse.wst.server.core" common
%mvn_package ":org.eclipse.wst.server.discovery" common

# Server Tools features and plugins
%mvn_package "org.eclipse.webtools.servertools:" servertools

# Source Editing features and plugins
%mvn_package "org.eclipse.webtools.jsdt*:" sourceediting
%mvn_package "org.eclipse.webtools.sourceediting:" sourceediting
%mvn_package ":org.eclipse.wst.web{,.ui,.ui.infopop}" sourceediting

# Java EE features and plugins
%mvn_package "org.eclipse.webtools.ejb:" javaee
%mvn_package "org.eclipse.webtools.javaee:" javaee
%mvn_package "org.eclipse.webtools.webservices:" javaee

# JSF features and plugins
%mvn_package "org.eclipse.webtools.jsf:" jsf

# Dali features and plugins
%mvn_package "org.eclipse.webtools.dali:" dali
%mvn_package "org.eclipse.persistence:" dali

# Fix version restriction on rhino and gson
for mf in $(find -name MANIFEST.MF -exec grep -l "org.mozilla.javascript" {} \;) ; do
  sed -i -e '/org.mozilla.javascript/s/1\.7\.5/1.7.2/' $mf
done
for mf in $(find -name MANIFEST.MF -exec grep -l "com.google.gson" {} \;) ; do
  sed -i -e '/com.google.gson/s/2\.2\.4/2.2.2/' $mf
done
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_build -j -f -- -DforceContextQualifier=%{qualifier}
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install

# TODO: figure why this is incorrectly generated for rh-java-common namespace
sed -i -e 's/\(org\.mozilla\.javascript\)(rh-java-common)/\1/' \
  %{buildroot}%{_datadir}/maven-metadata/eclipse-webtools-sourceediting.xml
%{?scl:EOF}


# The following scriptlets install OSGi runtime extension hooks
# It must be in the same directory as the system bundle to work
# For details, see: https://wiki.eclipse.org/Adaptor_Hooks

%post sourceediting
if [ -e %{_prefix}/lib64/eclipse ] ; then
  pushd %{_prefix}/lib64/eclipse/plugins 2>&1 >/dev/null
else
  pushd %{_prefix}/lib/eclipse/plugins 2>&1 >/dev/null
fi
rm -f org.eclipse.wst.jsdt.nashorn.extension_*
ln -s %{_datadir}/eclipse/droplets/webtools-sourceediting/eclipse/plugins/org.eclipse.wst.jsdt.nashorn.extension_*
popd 2>&1 >/dev/null

%postun sourceediting
if [ -e %{_prefix}/lib64/eclipse ] ; then
  rm %{_prefix}/lib64/eclipse/plugins/org.eclipse.wst.jsdt.nashorn.extension_*
else
  rm %{_prefix}/lib64/eclipse/plugins/org.eclipse.wst.jsdt.nashorn.extension_*
fi

%files common -f .mfiles-common
%doc webtools.common/features/org.eclipse.jst.common_core.feature.patch/epl-v10.html

%files servertools -f .mfiles-servertools

%files sourceediting -f .mfiles-sourceediting

%files javaee -f .mfiles-javaee

%files jsf -f .mfiles-jsf

%if %{with datatools}
%files dali -f .mfiles-dali
%endif

%changelog
* Tue Aug 16 2016 Mat Booth <mat.booth@redhat.com> - 3.8.0-1.3
- Fix breakpoint inteference with CDT, rhbz#1367019

* Mon Aug 01 2016 Mat Booth <mat.booth@redhat.com> - 3.8.0-1.2
- Disable features that require datatools, which is not yet available
- Fix version requirements of rhino and gson
- Patch to accomodate older jetty
- Filter out incorrect auto-requires on rhino

* Mon Aug 01 2016 Mat Booth <mat.booth@redhat.com> - 3.8.0-1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Tue Jul 05 2016 Mat Booth <mat.booth@redhat.com> - 3.8.0-1
- Update to tagged version
- Drop ancient provides/obsoletes
- Merge some sub-packages to eliminate cyclical deps and simplify
  the packaging a little bit
- Rationalise BRs and Rs

* Wed Jun 1 2016 Alexander Kurtakov <akurtako@redhat.com> 3.8.0-0.1gitb640484
- Update to Neon pre release.

* Tue Feb 09 2016 Roland Grunberg <rgrunber@redhat.com> - 3.7.1-3
- Update to use proper xmvn provided macros.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Oct 03 2015 Gerard Ryan <gerard@ryan.lt> - 3.7.1-1
- Update to latest upstream release tag R3_7_1 for Mars.1

* Sun Sep 13 2015 Gerard Ryan <gerard@ryan.lt> - 3.7.0-1
- Update to latest upstream release tag R3_7_0 for Mars

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Gerard Ryan <gerard@ryan.lt> - 3.6.3-2
- Update to latest upstream release tag R3_6_3

* Sat Jan 24 2015 Gerard Ryan <gerard@ryan.lt> - 3.6.2-1
- Update to latest upstream release tag R3_6_2

* Thu Dec 11 2014 Alexander Kurtakov <akurtako@redhat.com> 3.6.1-3
- Remove unneeded BR on feclipse-maven-plugin.

* Tue Nov 18 2014 Alexander Kurtakov <akurtako@redhat.com> 3.6.1-2
- Fix typo in webtools-servertools installation.

* Fri Sep 26 2014 Gerard Ryan <gerard@ryan.lt> - 3.6.1-1
- Update to latest upstream release tag R3_6_1

* Fri Aug 22 2014 Mat Booth <mat.booth@redhat.com> - 3.6.0-7
- Prefix qualifier to ensure it is lexographically greater than the
  upstream's update site (prevents unnecessary updates)
- Make use of build-jar-repository and build-classpath utils

* Tue Aug 12 2014 Gerard Ryan <gerard@ryan.lt> - 3.6.0-6
- Use forceContextQualifier instead of git

* Sat Jul 19 2014 Gerard Ryan <gerard@ryan.lt> - 3.6.0-5
- Add features from webtools.webservices.jaxws

* Sun Jul 06 2014 Gerard Ryan <gerard@ryan.lt> - 3.6.0-4
- Add missing Obsoletes for old sdk packages

* Thu Jul 03 2014 Gerard Ryan <gerard@ryan.lt> - 3.6.0-3
- Add missing BRs

* Tue Jul 01 2014 Gerard Ryan <gerard@ryan.lt> - 3.6.0-2
- Initial RPM
